import cv2 as cv
import numpy as np
import pca

def main():
     arquivo_a_reduzir = 'test0'
     numero_de_features_apos_PCA = 100
     cnn_flow = pca.read_cnnf_file(arquivo_a_reduzir)
     cnn_flow_padronizado = pca.cnn_flow_para_PCA(cnn_flow)
     numero_de_samples = len(cnn_flow_padronizado)
     cnn_flow_conformado = pca.conformar_cnn_flow_para_PCA(cnn_flow_padronizado)
     auto_vetores, media = pca.baseground_PCA(cnn_flow_conformado,numero_de_features_apos_PCA)
     pca.write_pca_baseground("autovetores", auto_vetores)
     pca.write_pca_baseground("vetor_media", media)
     projecao = pca.projecao_PCA(cnn_flow_padronizado, media, auto_vetores)
     pca.write_pca_reduction(arquivo_a_reduzir,projecao)
if __name__ == '__main__':
     main()
