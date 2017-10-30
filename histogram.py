import argparse
import cv2
import numpy as np
import os
from scipy.cluster.vq import kmeans2, vq

encode = "utf-8"

def _get_Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("name", help="Video file name reduced by pca")
	parser.add_argument("codedir", help="Directory of codebooks")
	parser.add_argument("-o", "--outdir", help="Output directory")
	return parser.parse_args()

def read_pca(name):

	try:
		with open(name, "r", encoding=encode) as file:
			# Quebro por fragmentos, depois por linha, e depois por valor
			pca_features = [[[float(item) if item != '' else 0.0 for item in line.split(" ") ] for line in snippet.split(" \n")] for snippet in file.read().split(" \n\n")]
			# Ultimo elemento sempre fica vazio por causa do ultimo \n
			del pca_features[-1]
			#videos.append(pca_features)
		
		return np.array(pca_features)
		
	except Exception as e:
		print("A problem occurred trying to read pca file: ", e)
		print("With parameters: \n", vars(args))
		return 0
		
def read_codebooks(dir):

	try:
		'''
		Para cada arquivo no diretorio dir, faco o split do nome do arquivo por '.' (ponto) e, se o ultimo elemento apos o split for a 
		extensao que desejo, o nome o arquivo sera concatenado com o diretorio e vai compor a lista de nomes dos arquivos que serao abertos
		'''
		names = [os.path.join(dir, file) for file in os.listdir(dir) if file.split('.')[-1] == 'dic']
		codebooks = []
		
		for name in names:
			with open(name, "r", encoding=encode) as file:
				# Quebro por pontos e depois por valor
				cluster = [[float(value) if value != '' else 0.0 for value in point.split(" ")] for point in file.read().split("\n")]
				# Ultimo elemento sempre fica vazio por causa do ultimo \n
				#del cluster[-1]
				codebooks.append(cluster)
		
		return codebooks
		
	except Exception as e:
		print("A problem occurred trying to read pca file: ", e)
		print("With parameters: \n", vars(args))
		return 0
		
def get_levels(n):
	
	if n == 17:
		return 4
		
	elif n == 7:
		return 3
		
	elif n == 3:
		return 2
		
	elif n == 1:
		return 1
	else:
		return 0
		
def get_interval_by_level(n):

	if n == 0:
		return 0, 1
		
	elif n == 1:
		return 1, 3
		
	elif n == 2:
		return 3, 7
		
	elif n == 3:
		return 7, 17
	else:
		return 0,0
		
	
def create_histograms(pca, codebooks):
	
	num_snippet  = len(pca)
	num_snip_feat = len(pca[0])
	num_levels = get_levels(num_snip_feat)
	
	# Crio um np.array com dimensoes numero de niveis e quantidade de pontos por cluster
	histograms = np.zeros((num_levels, len(codebooks[0])), "float32")
	
	# Para cada level
	for i in range(num_levels):
		# Descubro as linhas que correspondem ao nivel atual
		begin, end = get_interval_by_level(i)
		# Inicializo o empilhamento de descritores
		descriptors = np.array(pca[0][begin:end])
		# Para cada snippet do video
		for j in range(num_snippet):
			# Se nao for aquele primeiro que ja empilhei na inicializacao
			if not (j == 0):
				# Transformo os descritores para esse nivel em um np.array
				descriptor = np.array(pca[j][begin:end])
				# Empilho os descritores
				descriptors = np.vstack((descriptors, descriptor))
				
		words, distance = vq(descriptors, codebooks[i])
		for w in words:
			histograms[i][w] += 1
		

	return histograms
	
def write_histograms(name, outdir, histograms):

	name = os.path.split(name)[1]
	name = name.split('.')[0]
	
	try:	
		# If path doesn't exists, make it
		if not os.path.isdir(outdir):
			os.makedirs(outdir)

		out_file = os.path.join(outdir, name) + ".desc"
			
		# With automatically closes output
		with open(out_file, "w", encoding=encode) as output:
			# Joining 
			output.write("\n".join([" ".join(list(map(str, line))) for line in histograms.tolist()]))
		
		return 0
		
	except Exception as e:
		print("Some error occurred while writing histogram into file: ", e)
		return 1
	
def _main(args):
	
	pca = read_pca(args.name)
	codebooks = read_codebooks(args.codedir)
	histograms = create_histograms(pca, codebooks)
	if not args.outdir:
		args.outdir = ''
	
	write_histograms(args.name, args.outdir, histograms)
	
	
if __name__ == '__main__':
	# parse arguments
	args = _get_Args()
	_main(args)
