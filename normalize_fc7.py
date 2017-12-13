import argparse
import numpy as np
import os
import time
from multiprocessing import Pool
#from binary_features import read_fc7_file
import norma_fc7
from algeb import normalizar
import pandas as pd
import norma_fc7 as nfc7

encode = "utf-8"
threads_file = 'threads.txt'

def _get_Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("indir", help="Directory with all fc7 dataset splitted in traning, validation and test folders")
	parser.add_argument("outdir", help="Output directory to write the normalized features")
	parser.add_argument("type", help="Normalization type", choices=['max_min', 'standard'])
	return parser.parse_args()
	
def get_threads():

	try:
		with open(threads_file, "r", encoding=encode) as input:
			# Reading number of threads
			threads = int(input.read())
			return threads
	except Exception as e:
		print("A problem ocurred trying to read the number of threads: ", e)

def read_fc7_file(name):

	#print(str(name))
	#if not str(name).endswith('.fc7'):
	fc7_file = str(name) 
	#else:
		#fc7_file = str(name)
	fc7 = open(fc7_file, "r", encoding=encode)
	
	#list with frame features
	frames = fc7.readlines()
	fc7.close()
	return frames
		
def max_min_fc7_local(name):

	# Reading fc7 file
	fc7 = read_fc7_file(name)
	# l2 normalization
	#fc7 = np.array([normalizar(frame) for frame in fc7])
	# Getting the number of frames
	#frames = fc7.shape[0]
	# Element-wise sum
	#fc7_sum = np.sum(fc7, 0)
	# Element-wise max
	fc7_max = np.max(fc7, 0)
	# Element-wise min
	fc7_min = np.min(fc7, 0)
	#return fc7_sum, fc7_max, fc7_min, frames
	return fc7_max, fc7_min
	
def sum_max_min_fc7_global(name):
	sum, max, min, frames = sum_max_min_fc7_local(name)
	frames = frames * sum.shape[0]
	max = np.max(max)
	min = np.max(min)
	sum = np.sum(sum)
	return sum, max, min, frames
	
def write_fc7(name, fc7):
	df = pd.DataFrame(fc7)
	df.to_csv(name, sep=',', line_terminator='\n', encoding=encode, header=None, index=False)
	
def write_max_min(in_name, out_name, max, min):
	fc7 = read_fc7_file(in_name)# Reading fc7 file
	fc7 = norma_fc7.norma_max_min(fc7, max, min) # Applying max min normalization
	write_fc7(out_name, fc7) # Writing data
	
def converter_vetor(vetor):
	vetor_convertido = np.array(vetor,'float32')
	return vetor_convertido
	
def valor_esperado(pagina): # retorna a norma média em uma pagina. Leia-se um arquivo com vetores como página
	pagina = np.array(pagina,'float32')
	lista_de_normas = []
	for vetor in pagina:
		lista_de_normas.append(normalizar(vetor))
	n_elementos = len(pagina)
	media = np.mean(lista_de_normas)
	return media, n_elementos

def quadrado(lista):
	lista = np.array(lista,'float32')
	quadrado = np.power(lista,2)
	return quadrado

def det_param(nome_arquivos):
	media_global = 0
	quadrado_global = 0
	n_elementos_total = 0
	for i in nome_arquivos:
		arquivo = read_fc7_file(i)
		media, n_elementos_local = valor_esperado(read_fc7_file(arquivo))
		quadrado_global = quadrado_global + np.sum(quadrado(arquivo));	
		media_global = media_global + media*n_elementos_local
		n_elementos_total = n_elementos_total + n_elementos_local
	media = media_global/n_elementos_total
	media_dos_quadrados = quadrado_global/n_elementos_total
	desvio_padrao = power( media_dos_quadrados - power(media,2) , 0.5 )
	return media, desvio_padrao

def normalize(type, indir, outdir):
	# Listing files inside training
	in_fc7_files = {'training':[], 'validation':[], 'test':[]}
	out_fc7_files = {'training':[], 'validation':[], 'test':[]}
	for set in ['training', 'validation', 'test']:	
		
		# reading fc7 filenames
		dir = os.path.join(indir, set)
		fc7_files = [file for file in os.listdir(dir) if os.path.splitext(file)[1] == '.fc7']
		# joinning with input dir
		in_fc7_files[set] = [os.path.join(dir, file) for file in fc7_files]
		# joining with output dir
		dir = os.path.join(outdir, set)
		if not os.path.isdir(dir):
			os.makedirs(dir, exist_ok = True)
		out_fc7_files[set] = [os.path.join(dir, file) for file in fc7_files]	
	#debug
	'''
	print(in_fc7_files['training'])
	print(in_fc7_files['training'][0])
	print(type(in_fc7_files))
	'''
	#end debug
	if type == 'max_min':
		max, min = max_min_fc7_local(in_fc7_files['training'][0])
		global_max = np.array(max)
		global_min = np.array(min)
		for i in range(1, len(in_fc7_files['training'])):
			max, min = max_min_fc7_local(in_fc7_files['training'][i])
			global_max = np.max(np.vstack((global_max, max)), 0)
			global_min = np.min(np.vstack((global_min, min)), 0)
		
		for set in ['training', 'validation', 'test']:	
			for infile, outfile in zip(in_fc7_files[set], out_fc7_files[set]):
				write_max_min(infile, outfile, global_max, global_min)
		
	elif type == 'standard':
		
		media, desvio_padrao = det_param(in_fc7_files['training'])
		'''
		print('atual: normalize')
		'''
		
		for arq in in_fc7_files['training']:
			arquivo = read_fc7_file(arq)
			vetor_normalizado = []
			for vetor in arquivo:
				vetor_normalizado.append(nfc7.norma_estatistica_padrao(vetor,media,desvio_padrao))
			vetor_normalizado = np.array(vetor_normalizado,'float32') # casting para nparray
			write_fc7(out_fc7_files,vetor_normalizado)
			
	
def _main(args):
	normalize(args.type, args.indir, args.outdir)
	
if __name__ == '__main__':
	# parse arguments
	args = _get_Args()
	_main(args)
	
	print('depois')