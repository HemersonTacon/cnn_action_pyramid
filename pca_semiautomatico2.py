'''
Takes a path as input (where the cnnf are), then, based on an eigenvector matriz and a mean vector,
PCA projection is performed
INPUT:  Path to the cnn flow files to be reduced; # dimension to be reduced to; path to mean vect and eig mat
OUTPUT: Projected cnn flow
Arguments:
* Path to the Cnn Flow to be reduced
* Number os dimensions after reduction
* Path to the folder that contains the mean and the eigenvectors whose projection is performed into
* Path to the output directory
'''

import cv2 as cv
import numpy as np
import pca
import argparse
import os 

def _get_Args():
     parser = argparse.ArgumentParser()
     parser.add_argument("path", help="Path to file to be reduced")
     parser.add_argument("features",type=int, help="Number of features to be reduced to")
     parser.add_argument("read",help="path where the mean ans the eigenvector will be read from \n Notice, files must be names as 'mean.pcab' and 'eigenVectors.pcab'")
     parser.add_argument("outdir", help="Output directory")
     return parser.parse_args()

def _main(args):
     path2project = args.path
     files = os.listdir()
     for i in range(len(files))

          if '.cnnf' in files[k]

               files2project = os.path.join(path,files[k]) #getings the path + file's name, os the vector to be reduced (projected)
               nfeatures_after_PCA = args.features
               cnn_flow = pca.read_file(file2project) #reading the content fo the file
               cnn_flow_padronizado = pca.file2PCA(cnn_flow) #conforming it to apply PCA 
               #/fetch eigenVectors
               file_eg = open(args.read + 'eigenVectors.pcab', "r" )
               lines = file_eg.readlines()
               file_eg.close()
               eigenVectors = pca.file2PCA(lines)
               #/fetch mean
               file_mean = open(args.read+'mean.pcab',"r")
               lines = file_mean.readlines()
               file_mean.close()
               mean = pca.file2PCA(lines)
               #/computing projection
               projection = pca.projecao_PCA(cnn_flow_padronizado, mean, eigenVectors)
               #/saving file
               pca.write_pca_reduction(files[k],projection,args.outdir)

if __name__ == '__main__':
     args = _get_Args()
     _main(args)
