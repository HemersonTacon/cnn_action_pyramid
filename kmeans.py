import argparse
import cv2
import numpy as np
import os
from scipy.cluster.vq import kmeans2, vq
from sklearn import metrics, cluster

encode = "utf-8"

def get_Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("dir", help="Directory of dataset reduced by pca")
	parser.add_argument("size", type=int, help="Size of codebook")
	parser.add_argument("-o", "--outdir", help="Output directory")
	parser.add_argument("-i", "--iterations", help="Number of iterations of kmeans algorithm")
	return parser.parse_args()

def read_pca(dir):

	try:
		'''
		Para cada arquivo no diretorio dir, faco o split do nome do arquivo por '.' (ponto) e, se o ultimo elemento apos o split for a 
		extensao que desejo, o nome o arquivo sera concatenado com o diretorio e vai compor a lista de nomes dos arquivos que serao abertos
		'''
		names = [os.path.join(dir, file) for file in os.listdir(dir) if file.split('.')[-1] == 'pca']
		videos = []
		
		for name in names:
			with open(name, "r", encoding=encode) as file:
				# Quebro por fragmentos, depois por linha, e depois por valor
				pca_features = [[[float(item) if item != '' else 0.0 for item in line.split(" ") ] for line in snippet.split(" \n")] for snippet in file.read().split(" \n\n")]
				# Ultimo elemento sempre fica vazio por causa do ultimo \n
				del pca_features[-1]
				videos.append(pca_features)
		
		return np.array(videos)
		
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
		
	
def create_codebooks(pca_videos, size, iter):
	
	print("Shape: ", pca_videos.shape)
	num_videos  = pca_videos.shape[0]
	num_snip_feat = len(pca_videos[0][0])
	num_levels = get_levels(num_snip_feat)
	
	codebooks = []
	
	# Para cada level
	for i in range(num_levels):
		# Inicializo o empilhamento de descritores
		descriptors = np.array(pca_videos[0][0][0])
		# Para cada video
		for j in range(num_videos):
			# Para cada snippet do video
			for k in range(len(pca_videos[j])):
				# Se nao for aquele primeiro que ja empilhei na inicializacao
				if not (j == 0 and k == 0 and i == 0):
					# Tranformo o snippet inteiro em um np.array
					descriptor = np.array(pca_videos[j][k])
					# Descubro as linhas que correspondem ao nivel atual
					begin, end = get_interval_by_level(i)
					# Empilho os descritores referentes ao nivel atual
					descriptors = np.vstack((descriptors, descriptor[begin:end]))
		# Rodo o kmeans pra um nivel
		# Em ordem os parâmetros passados são: dados, numero de clusters, 
		#model = cluster.KMeans(n_clusters=size, max_iter=iter).fit(descriptors)
		centroids, labels = kmeans2(descriptors, size, iter, minit='random', missing='warn')
		#voc, variance = kmeans(descriptors, size, iter)
		#labels = model.labels_
		#centroids = model.cluster_centers_
		codebooks.append(centroids)
		score = metrics.silhouette_score(descriptors, labels, metric='euclidean')
		print("Silhouette coefficient of codebook ",i,": ", score)

	return codebooks
	
def write_codebooks(outdir, codebooks):

	name = "codebook"
	
	try:	
		# If path doesn't exists, make it
		if not os.path.isdir(outdir):
			os.makedirs(outdir)

		for i in range(len(codebooks)):
			out_file = os.path.join(outdir, name) + str(i) + ".dic"
	
			# With automatically closes output
			with open(out_file, "w", encoding=encode) as output:
				# Casting np.array to list then cast elements to str, join them with space and finally join rows with \n
				output.write("\n".join([" ".join(list(map(str, line))) for line in codebooks[i].tolist()]))
			
		return 0
		
	except Exception as e:
		print("Some error occurred while writing codebook into file: ", e)
		return 1
	
def main(args):
	
	pca_videos = read_pca(args.dir)
	if not args.iterations:
		args.iterations = 1000
	codebooks = create_codebooks(pca_videos, args.size, args.iterations)
	if not args.outdir:
		args.outdir = ''
	
	write_codebooks(args.outdir, codebooks)
	
	
if __name__ == '__main__':
	# parse arguments
	args = get_Args()
	main(args)
