import argparse
import cv2
import numpy as np
import os
from kmeans import read_pca, create_codebooks, write_codebooks
from histogram import create_histograms, write_histograms

encode = "utf-8"

def get_Args():
	parser = argparse.ArgumentParser()
	parser.add_argument("dir", help="Directory of dataset reduced by pca")
	parser.add_argument("size", type=int, help="Size of codebook")
	parser.add_argument("-o", "--outdir", help="Output directory")
	parser.add_argument("-s", "--savecodes", help="If present the codebooks will be saved in disk", action = 'store_true')
	parser.add_argument("-i", "--iterations", help="Number of iterations of kmeans algorithm")
	return parser.parse_args()
	
def create_all_histograms(pca_videos, codebooks):

	histograms_videos = []
	
	for pca in pca_videos:
		histograms = create_histograms(pca, codebooks)
		histograms_videos.append(histograms)
		
	return histograms_videos
		
def write_all_histograms(dir, histograms_videos, outdir):
	
	names = [os.path.join(dir, file) for file in os.listdir(dir) if file.split('.')[-1] == 'pca']
	
	for name, histograms in zip(names, histograms_videos):
		write_histograms(name, outdir, histograms)
		
def main(args):

	pca_videos = read_pca(args.dir)
	
	if not args.iterations:
		args.iterations = 50
		
	codebooks = create_codebooks(pca_videos, args.size, args.iterations)
	
	if not args.outdir:
		args.outdir = ''
	
	if args.savecodes:
		write_codebooks(args.outdir, codebooks)
	
	codebooks = [codebook.tolist() for codebook in codebooks]
	
	histograms_videos = create_all_histograms(pca_videos, codebooks)
	
	write_all_histograms(args.dir, histograms_videos, args.outdir)
	
	
	
if __name__ == '__main__':
	# parse arguments
	args = get_Args()
	main(args)
