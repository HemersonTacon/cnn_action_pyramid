'''
gather all the files, of all classes, of a specified level.
Then  a PCA basis is found for this files
INPUT: CNN Flow, press -h for more info on the console
OUTPUT: PCA autovector e mean at the cnnf folder
ARGUMENTS:
*path to the cnn flows
*name of the folder of the desired elvel
*class 1 folder
*class 2 folder
*class 3 folder
*class 4 folder
*class 5 folder
*class 6 folder
'''

import cv2 as cv
import numpy as np
import pca
import argparse
import os

def _get_Args():

     parser = argparse.ArgumentParser()
     parser.add_argument("path", help="path containing all the descriptors folders")
     parser.add_argument("level",help="folder's name level")
     parser.add_argument("class1", help="read class 1")
     parser.add_argument("--class2","-c2", help="read class 2")
     parser.add_argument("--class3","-c3", help="read class 3")
     parser.add_argument("--class4","-c4", help="read class 4")
     parser.add_argument("--class5","-c5", help="read class 5")
     parser.add_argument("--class6","-c6", help="read class 6")
     return parser.parse_args()

def read_file(name):

     desc = open(name, "r")
     descriptor = desc.readlines()
     desc.close()
     return descriptor
     
def concat_base():

     group = []
     file_path = args.path
     full_file_path = []
     level = args.level
     group.append(args.class1)
     if args.class2 != None:

          group.append(args.class2)
     if args.class3 != None:

          group.append(args.class3)
     if args.class4 != None:

          group.append(args.class4)
     if args.class5 != None:

          group.append(args.class5)
     if args.class6 != None:

          group.append(args.class6)
          
     caminho = []
     cnnFlow = []
     #providing a path for each class in a dataset
     for i in range (len(group)):

          temp = os.path.join(file_path,group[i])
          temp = os.path.join(temp,level)
          full_file_path.append(temp)

     '''**************************************************************'''     

     allCnnFlow = np.array([],'float32')
     debug_cont = 0
     not_first_time = False
     for h in range(len(group)):

          print('Current class\'s path :')
          print(full_file_path[h])
          for i in os.listdir(full_file_path[h]): # laço para o numero de arquivos que tem na pasta ( todas as pastas tem o mesmo numeor de arquivos)
               
               complete_path =  os.path.join(full_file_path[h],i)
               cnnFlow = read_file(complete_path)
               cnnFlow2 = pca.file2PCA(cnnFlow)
               if not_first_time:

                    allCnnFlow = np.append(allCnnFlow,cnnFlow2,axis=0)
               else:

                    allCnnFlow = cnnFlow2     
               debug_cont +=1          
               not_first_time = True
     return allCnnFlow

def _main(args):

     allCnnFlow = concat_base()
     cnnFlow_conformed = pca.conform2PCA(AllCnnFlow)
     n_features_after_PCA = 100
     print('Wait! can take a little while to get it done')
     eigenVectors, mean = pca.baseground_PCA(cnnFlow_conformed,n_features_after_PCA)
     print('Done!') 
     print(eigenVectors.shape)
     pca.write_pca_baseground('mean',args.level, mean, args.path)
     pca.write_pca_baseground('eigenVectors',args.level, eigenVectors, args.path)
     

if __name__ == '__main__':

     args = _get_Args()
     _main(args)
