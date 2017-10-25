import cv2 as cv
import numpy as np

global numeroDeFeaturesPrePCA
global numero_de_features_apos_PCA
numero_de_features_apos_PCA = 180


encode = "utf-8"


def read_cnnf_file(name):
     cnnf_file = name + ".cnnf"
     cnnf = open(cnnf_file, "r")
     cnnFlows = cnnf.readlines()
     cnnf.close()
     return cnnFlows


def auto_vetores_e_media_PCA(vetor_para_PCA,numero_de_features_apos_PCA):
     media, autoVetores = cv.PCACompute(vetor_para_PCA, None , None, numero_de_features_apos_PCA)
     return autoVetores, media

def projecao_PCA(vetor_para_PCA, media, auto_vetores):
     projecao = cv.PCAProject(vetor_para_PCA, media, auto_vetores)
     return projecao

def back_projecao_PCA(projecao, media, auto_vetores):
     back_projecao = cv.PCABackProject(projecao, media, auto_vetores)
     return back_projecao

def erro_medio_de_projecao(vetor_para_PCA,back_projecao):
     erro = vetor_para_PCA - back_projecao
     erro_quadratico_medio = np.mean(np.power(erro,2))
     return erro_quadratico_medio
    	
def write_cnn_flow(name, cnn_flow_PCA):

     out_file = name + ".pca"
	
     # With automatically closes output
     with open(out_file, "w", encoding=encode) as output:
	  # Joining cnn flows elements with space and then joining cnn flows with \n and finally joining snippets with \n\n
               output.write("\n\n".join(["\n".join([" ".join(list(map(str, j))) for j in i]) for i in cnn_flow_PCA]))


#nao
def write_pca_reduction(name, outdir, cnnFlowPCA):

     out_file = outdir + name + ".pca"
     with open(out_file, "w", encoding=encode) as output:
     # Joining frames binary coded with \n
          output.write("\n".join(cnnFlowPCA))

def cnn_flow_para_PCA(cnn_flow):
     global numero_de_features_antes_do_PCA
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
     return vetor_para_PCA

def main():
     
     cnn_flow = read_cnnf_file("cnnflows")
     vetor_para_PCA = cnn_flow_para_PCA(cnn_flow)
     auto_vetores, media = auto_vetores_e_media_PCA(vetor_para_PCA,numero_de_features_apos_PCA)
     projecao = projecao_PCA(vetor_para_PCA, media, auto_vetores)
     back_projecao = back_projecao_PCA(projecao, media, auto_vetores)
     erro_quadratico_medio = erro_medio_de_projecao(vetor_para_PCA,back_projecao)
     print(erro_quadratico_medio)     
if __name__ == '__main__':
     main()
