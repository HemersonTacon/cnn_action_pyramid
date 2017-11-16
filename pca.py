import cv2 as cv
import numpy as np
import os

global numero_de_features_antes_do_PCA
global numero_de_features_apos_PCA  




encode = "utf-8"


def read_cnnf_file(name):
     cnnf_file = name
     cnnf = open(cnnf_file, "r")
     cnnFlows = cnnf.readlines()
     cnnf.close()
     return cnnFlows


def baseground_PCA(vetor_para_PCA, numero_de_features_apos_PCA):
     
     #print("\ncomputando os autovetores e o vetor de media... pode demorar...")
     #print("O numero de features apos PCA e de: " + str(numero_de_features_apos_PCA))
     media, autoVetores = cv.PCACompute(vetor_para_PCA, None , None, int(numero_de_features_apos_PCA))
     #print('\nautovetores e media obtidos com sucesso!')
     return autoVetores, media

def padrao_PCA(entrada):
     indice_i =  shape.entrada[0]
     indice_j =  len(entrada[0])
     saida = np.array((indice_i,indice_j))
     for i in range(entrada_i):
          for j in range(entrada_j):
               saida[i][j] = float(entrada[i][j])
     return saida

def projecao_PCA(vetor_para_PCA, media, auto_vetores):
     projecao = cv.PCAProject(vetor_para_PCA, media, auto_vetores)
     return projecao

def back_projecao_PCA(projecao, media, auto_vetores):
     back_projecao = cv.PCABackProject(projecao, media, auto_vetores)
     return back_projecao

def erro_medio_de_projecao(vetor_para_PCA,back_projecao):
     erro = (vetor_para_PCA - back_projecao)
     erro_quadratico_medio = np.mean(np.power(erro,2))
     return erro_quadratico_medio
    	
def write_pca_reduction(name, cnn_flow_PCA, outdir):
	
     if not os.path.isdir(outdir) and outdir !='':
	            os.makedirs(outdir)
				
     out_file = os.path.join(outdir, os.path.splitext(name)[0] + ".pca")
     # With automatically closes output
     with open(out_file, "w", encoding=encode) as output:
	  # Joining cnn flows elements with space and then joining cnn flows with \n and finally joining snippets with \n\n
               output.write("\n".join([" ".join(list(map(str,i))) for i in cnn_flow_PCA]))


def write_pca_baseground(name, baseground_PCA, outdir):
     
     if not os.path.isdir(outdir) and outdir !='':
	            os.makedirs(outdir)
				
     out_file = os.path.join(outdir, os.path.splitext(name)[0] + ".pcab")
     # With automatically closes output
     with open(out_file, "w", encoding=encode) as output:
	  # Joining cnn flows elements with space and then joining cnn flows with \n and finally joining snippets with \n\n
               output.write("\n".join([" ".join(list(map(str,i))) for i in baseground_PCA]))


     
def cnn_flow_para_PCA(cnn_flow):
     global numero_de_features_antes_do_PCA
     global numero_de_features_apos_PCA
     numero_de_features_apos_PCA = 100
     cnnFlowsSplit = []
     cnnFlowsSplitFloat = [[]]
     contador = -1
     
     for i in range(len(cnn_flow)):

          cnnFlowsSplit = cnn_flow[i].split( )
          if cnnFlowsSplit == []:

               continue
          contador = contador + 1
          cnnFlowsSplitFloat.append([]) # gerando um novo no para a lista

          for j in range (len(cnnFlowsSplit)): # casting

               cnnFlowsSplitFloat[contador].append( float(cnnFlowsSplit[j]))  

     del cnnFlowsSplitFloat[len(cnnFlowsSplitFloat) - 1] # REMOVENDO O NO EXTRA GERADO
     vetor_para_PCA = np.array(cnnFlowsSplitFloat)
     numero_de_features_antes_do_PCA= len(vetor_para_PCA[0])
   #  numero_de_features_apos_PCA = numero_de_features_antes_do_PCA/2 #voltar depois para 180
     return vetor_para_PCA

'se tiver menos cNN Flows que features, copiar os videos até ter mais videos que CNN flows'
def conformar_cnn_flow_para_PCA(vetor_para_PCA):

     vetor_para_PCA_fixo = np.copy(vetor_para_PCA)
     folga = 5
     cont = 0
     if  len(vetor_para_PCA) <= len(vetor_para_PCA_fixo[0]) + folga: # se tiver menos cnn FLows que features

          while len(vetor_para_PCA) <= len(vetor_para_PCA_fixo[0]) + folga:
     
               cont = cont + 1
               vetor_para_PCA = np.append(vetor_para_PCA,vetor_para_PCA_fixo,axis=0)

     return vetor_para_PCA

def _main():
     global numero_de_features_antes_do_PCA
     global numero_de_features_apos_PCA
     cnn_flow = read_cnnf_file("test0")
     print('O tipo do arquivo lido do cnnflow é:' + str(type(cnn_flow)))
     
     vetor_para_PCA = cnn_flow_para_PCA(cnn_flow)
     print('o numero de samples é: ' + str(len(vetor_para_PCA)))
     #print('A dimensao do cnn_flow convertido é de ' + str(len(vetor_para_PCA)) + 'linhas e ' + str(len(vetor_para_PCA[0])) + ' colunas e uma terceira dimensao de tamanho: ')
     vetor_para_PCA = conformar_cnn_flow_para_PCA(vetor_para_PCA)
     print('A dimensao do cnn_flow conformado  é de ' + str(len(vetor_para_PCA)) + 'linhas e ' + str(len(vetor_para_PCA[0])) + ' colunas e uma terceira dimensao de tamanho: ')# + str(len(vetor_para_PCA[0][0]))   )
     #print(vetor_para_PCA.shape)
     #print(len(vetor_para_PCA))
     #print(len(vetor_para_PCA[0]))
     #print("Numero de features antes do PCA: " + str(numero_de_features_antes_do_PCA))
     #print("Numero de features apos o PCA: " + str(numero_de_features_apos_PCA))

     auto_vetores, media = baseground_PCA(vetor_para_PCA,numero_de_features_apos_PCA)
     print('A dimensao de auto_vetores  é de ' + str(len(auto_vetores)) + ' linhas e ' + str(len(auto_vetores[0])) + 'colunas' )
     #print("baseground obtido!")
     write_pca_baseground("autovetores", auto_vetores)
     write_pca_baseground("vetor_media", media)
     #print('a dimensao de uma linha e de: ' + str(len(vetor_para_PCA[0])))
     #print(vetor_para_PCA[0])
     
     
     projecao = projecao_PCA(vetor_para_PCA[0:1][:], media, auto_vetores)
     #projecao = cv.PCAProject(vetor_para_PCA[], media, auto_vetores)
     #print(projecao)
     print(str(projecao.shape))
     write_pca_reduction('teste_projecao',projecao)
     back_projecao = back_projecao_PCA(projecao, media, auto_vetores)
    # erro_quadratico_medio = erro_medio_de_projecao(vetor_para_PCA,back_projecao)

     
if __name__ == '__main__':
     _main()
