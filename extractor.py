"""
Extractor is an image extractor specialization of Net.
"""

import numpy as np
import os
import sys
import argparse
import glob
import time
import caffe

class Extractor(caffe.Net):

	def __init__(self, model_file, pretrained_file, image_dims=None,
			mean=None, input_scale=None, raw_scale=None,
			channel_swap=None, layer=None):

		caffe.Net.__init__(self, model_file, pretrained_file, caffe.TEST)	
		#preprocessing definitions
		self.transformer = caffe.io.Transformer({'data': self.blobs['data'].data.shape})
		self.transformer.set_transpose('data', (2, 0, 1))
		
		if(mean is not None):
			mean_ = np.load(mean).mean(1).mean(1)
			self.transformer.set_mean('data', mean_)
		if input_scale is not None:
			self.transformer.set_input_scale('data', input_scale)
		if raw_scale is not None:
			self.transformer.set_raw_scale('data', raw_scale)
		if channel_swap is not None:
			self.transformer.set_channel_swap('data', channel_swap)

		self.crop_dims = np.array(self.blobs['data'].data.shape[2:])
		if image_dims is None:
			image_dims = self.crop_dims
		else:
			image_dims = [int(s) for s in image_dims.split(',')]
		self.image_dims = image_dims
		
		if layer is None:
			layer = 'fc7'
		self.layer = layer

		if self.layer not in self.blobs:
			raise TypeError("Invalid layer name: " + layer)
			 
	
	def extract(self, input_file, ext=None, center=None):
		
		#Load input
		if input_file.endswith('npy'):
			inputs = np.load(input_file)
		elif os.path.isdir(input_file):
			if(ext is None):
				ext = 'png'
			inputs = [caffe.io.load_image(img)
                 		for img in glob.glob(input_file + '/*.' + ext)]
		else:
			inputs = caffe.io.load_image(input_file)
		
		input_ = np.zeros((len(inputs), self.image_dims[0], self.image_dims[1],inputs[0].shape[2]), dtype=np.float32)
		
		for i, img in enumerate(inputs):
			input_[i] = caffe.io.resize_image(img, self.image_dims)

		# Take center crop.
		if center is not None:
			center = np.array(self.image_dims) / 2.0
			crop = np.tile(center, (1, 2))[0] + np.concatenate([-self.crop_dims / 2.0,self.crop_dims / 2.0])
			crop = crop.astype(int)
			input_ = input_[:, crop[0]:crop[2], crop[1]:crop[3], :]
		
		outputs = np.zeros((len(inputs),4096))

		for i, img in enumerate(inputs):
			self.blobs['data'].data[...] = self.transformer.preprocess('data', input_[i])
			output = self.forward(end=self.layer)
			for ix,j in enumerate(self.blobs[self.layer].data[0]):
				outputs[i][ix] = j
			
			
		return outputs	
