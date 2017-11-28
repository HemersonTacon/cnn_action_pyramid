'''
This file contains a method to merge all level descriptors in one single file.
'''

import cv2 as cv
import numpy as np
import pca
import argparse
import os
from DescrFVEC import saveDescriptor


encode = "utf-8"


def _get_Args():
     parser = argparse.ArgumentParser()
     parser.add_argument("path", help="path containing all the descriptors folders")
     parser.add_argument("--outdir","-o", help="path containing merged descriptors", default = "all\\")
     parser.add_argument("--level_0", "-l0",help="level 0 folder's name", default = 'nivel0\\')
     parser.add_argument("--level_1", "-l1",help="level 1 folder's name", default = 'nivel1\\')
     parser.add_argument("--level_2", "-l2",help="level 2 folder's name", default = 'nivel2\\')
     parser.add_argument("--level_3", "-l3",help="level 3 folder's name", default = 'nivel3\\')
     return parser.parse_args()

def read_desc_file(name):
     
     desc = open(name, "r")
     descriptor = desc.readlines()
     desc.close()
     return descriptor

def concat_desc():
     path = args.path
     outdir = args.outdir
     level = []
     caminho = []
     level.append(args.level_0)
     level.append(args.level_1)
     level.append(args.level_2)
     level.append(args.level_3)
     

     for j in range(4): # um laço para cada nivel para obter o caminhos para as pastas de cada nivel

          caminho.append(str(path)+str(level[j])) # caminho para cada nivel

     for i in range (len(  os.listdir(  str(path) + str(level[0]) ))): # laço para o numero de arquivos que tem na pasta ( todas as pastas tem o mesmo numeor de arquivos)

          new_descriptor = [] #descritor com todos os nives
          for j in caminho: # percorrer os quatro niveis

               #descriptor: descritor de cada nivel
               descriptor = read_desc_file( j + os.listdir(j)[i] ) # leitura de cada um dos niveis do arquivo especificado
               for k in range(len(descriptor)):

                    new_descriptor.append(float(descriptor[k][0]))     

          new_descriptor_np = np.array( new_descriptor,'float32' )
          files_name = os.listdir(j)[i]
          #tirar sufixo
          esta_contido = '.avi3.desc' in files_name
          if esta_contido:
               files_name = files_name.split('.avi3.desc')[0]
          files_name = files_name + '.fvec'
          saveDescriptor(files_name, new_descriptor_np)#invoking method from descrFVEC, which automatically write the file

          '''
          file = open(outdir + files_name + '.fvec',"wb") # gravar no diretorio de saida com os nomes dos arquivos
          for i in range(new_descriptor_np.shape[1]): 
               to_write = bytes([new_descriptor[i]])
               file.write(to_write)
          file.close()
          '''
          del new_descriptor
     
def _main():
     concat_desc()

if __name__ == '__main__':
     args = _get_Args()
     _main()
