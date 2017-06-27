import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
import math
import random
import os
import json
from numpy import matrix
from math import pow
from collections import namedtuple

class OCRNeuralNetwork(object):
	LEARNING_RATE=0.1
	WIDTH_IN_PIXWLS=20
	path=os.getcwd()+'/show/nn.json'   #在工程中要注意文件的路径
	NN_FILE_PATH=path

	def __init__(self,HIDDEN_NODE_COUNT,DATA_MATRIX,DATA_LABELS,training_indices,use_file=True):
	    self.sigmoid=np.vectorize(self._sigmoid_scalar)
	    self.sigmoid_prime=np.vectorize(self._sigmoid_prime_scalar)
	    self._use_file=use_file
	    self.data_matrix=DATA_MATRIX
	    self.data_labels=DATA_LABELS

	    if (not os.path.isfile(OCRNeuralNetwork.NN_FILE_PATH) or not use_file):
		    self.theta1=self._rand_initiallize_weights(400,HIDDEN_NODE_COUNT)
		    self.theta2=self._rand_initiallize_weights(HIDDEN_NODE_COUNT,10)
		    self.input_layer_bias=self._rand_initiallize_weights(1,HIDDEN_NODE_COUNT)
		    self.hidden_layer_bias=self._rand_initiallize_weights(1,10)

		    TrainData=namedtuple('TrainData',['y0','label'])
		    self.train([TrainData(self.data_matrix[i],int(self.data_labels[i])) for i in training_indices])
		    self.save()
	    else:
		    self.load()
		

	def _rand_initiallize_weights(self,size_in,size_out):
		return [((x*0.12) -0.06) for x in np.random.rand(size_out,size_in)]

	def _sigmoid_scalar(self,z):
		return 1/(1+math.e** -z)

	def _sigmoid_prime_scalar(self,z):
		return self.sigmoid(z) * (1-self.sigmoid(z))

	def _draw(self, sample):
		pixelArray = [sample[j:j+self.WIDTH_IN_PIXELS] for j in xrange(0, len(sample), self.WIDTH_IN_PIXELS)]
		plt.imshow(zip(*pixelArray), cmap = cm.Greys_r, interpolation="nearest")
		plt.show()

	def train(self,training_data_array):
		print('调用train方法')
		for data in training_data_array:
			y1=np.dot(np.mat(self.theta1),np.mat(data['y0']).T)
			sum1 =y1+np.mat(self.input_layer_bias)
			y1=self.sigmoid(sum1)

			y2=np.dot(np.array(self.theta2),y1)
			y2=np.add(y2,self.hidden_layer_bias)
			y2=self.sigmoid(y2)

			actual_vals=[0]*10
			actual_vals[data['label']]=1
			output_errors=np.mat(actual_vals).T-np.mat(y2)
			hidden_errors=np.multiply(np.dot(np.mat(self.theta2).T,output_errors),self.sigmoid_prime(sum1))

			self.theta1+=self.LEARNING_RATE*np.dot(np.mat(hidden_errors),np.mat(data['y0']))
			self.theta2+=self.LEARNING_RATE*np.dot(np.mat(output_errors),np.mat(y1).T)
			self.hidden_layer_bias+=self.LEARNING_RATE*output_errors
			self.input_layer_bias+=self.LEARNING_RATE*hidden_errors
		print('train方法调用结束')

	def predict(self,test):
		print('调用predict方法')
		y1=np.dot(np.mat(self.theta1),np.mat(test).T)
		y1=y1+np.mat(self.input_layer_bias)
		y1=self.sigmoid(y1)

		y2=np.dot(np.array(self.theta2),y1)
		y2=np.add(y2,self.hidden_layer_bias)
		y2=self.sigmoid(y2)

		results=y2.T.tolist()[0]
		print('predict方法调用结束')
		print('the predict result is ',results.index(max(results)))
		return results.index(max(results))

	def save(self):
		if not self._use_file:
			return
		json_neural_network={
		"theta1":[np_mat.tolist()[0] for np_mat in self.theta1],
		"theta2":[np_mat.tolist()[0] for np_mat in self.theta2],
		"b1":self.input_layer_bias[0].tolist()[0],
		"b2":self.hidden_layer_bias[0].tolist()[0]
		};
		with open(OCRNeuralNetwork.NN_FILE_PATH,'w') as nnFile:
			json.dump(json_neural_network,nnFile)

	def load(self):
		if not self._use_file:
			return
		with open(OCRNeuralNetwork.NN_FILE_PATH) as nnFile:
			nn=json.load(nnFile)
		self.theta1=[np.array(li) for li in nn['theta1']]
		self.theta2=[np.array(li) for li in nn['theta2']]
		self.input_layer_bias=[np.array(nn['b1'][0])]
		self.hidden_layer_bias=[np.array(nn['b2'][0])]
	