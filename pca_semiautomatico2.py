import cv2 as cv
import numpy as np
import pca
import argparse

def _get_Args():
     parser = argparse.ArgumentParser()
     parser.add_argument("file", help="File to reduce")
     parser.add_argument("features",type=int, help="Number of features to be reduced to")
     parser.add_argument("read",help="path where the mean ans the eigenvector will be read from \n Notice, files must be names as 'mean.pcab' and 'eigenVectors.pcab'")
     parser.add_argument("outdir", help="Output directory")
     return parser.parse_args()

def _main(args):
     file2project = args.file
     nfeatures_after_PCA = args.features
     cnn_flow = pca.read_file(file2project)
     cnn_flow_padronizado = pca.file2PCA(cnn_flow)
     #/fetch eigenVectors
     file_eg = open(args.read+'eigenVectors.pcab',"r")
     lines = file_eg.readlines()
     file_eg.close()
     eigenVectors = pca.file2PCA(lines)
     #/fetch mean
     file_mean = open(args.read+'mean.pcab',"r")
     lines = file_mean.readlines()
     file_mean.close()
     mean = pca.file2PCA(lines)
     #/computing projection
     projec
     #/saving file
     pca.write_pca_reduction(file2project,projecao,args.outdir)

if __name__ == '__main__':
     args = _get_Args()
     _main(args)
