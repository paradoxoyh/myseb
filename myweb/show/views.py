from django.shortcuts import render,render_to_response
from django.template import Template, Context, RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from .OCR import OCRNeuralNetwork
import numpy as np
import os
import json


def show_info(request):
	t=get_template('show.html')
	return HttpResponse(t.render())


def req_form(request):
	t=get_template('form.html')
	return HttpResponse(t.render())


def search(request):
	if request.method=='GET':
		return HttpResponse('There is nothing')
	elif request.method=='POST':
		return HttpResponse('Your search key word is %s' % request.POST['q'])


def tpl(request):   #在模板中调用方法，context的字典不再需要用Context()调用，直接传入字典即可
	t=get_template('tpl.html')
	c={'method':method}
	return HttpResponse(t.render(c))


def ocr(request):
	t=get_template('ocr.html')
	return HttpResponse(t.render())


def handle(request):
	path=os.getcwd()    #只是当前进程的工作目录，在工程中要注意文件的路径
	path+='\show\dataLabels.csv'
	DATA_LABELS=np.loadtxt(open(path,'rb'))
	path=os.getcwd()
	path+='\show\data.csv'
	DATA_MATRIX=np.loadtxt(open(path,'rb'),delimiter=',')
	HIDDEN_NODE_COUNT=15
	DATA_MATRIX=DATA_MATRIX.tolist()
	DATA_LABELS=DATA_LABELS.tolist()
	
	nn=OCRNeuralNetwork(HIDDEN_NODE_COUNT, DATA_MATRIX, DATA_LABELS, list(range(5000)))
	response_code=200
	print(request.META['CONTENT_LENGTH'])
	#print(request.META['CONTENT_LENGTH'])  #..大写下划线。。。。。干力量
	#print(request.body)                    #在Django之后的版本中变成了body，使用POST会得到None，没有raw_post_data属性
	payload=json.loads(request.body.decode('utf-8'))
	if payload.get('train'):                #json数据是byte类型，这里需要转换，decode('utf-8')
		nn.train(payload['trainArray'])
		nn.save()
		return HttpResponse('1')
	elif payload.get('predict'):
		try:
			print('predict-function will be called soon')
			req={"type":"test","result":nn.predict(str(payload['image']))}
			x=json.dumps(req)
			x_byte=bytes(x)
			return HttpResponse(x_byte, content_type='test')    #这里还有一点点问题
		except Exception as e:
			print(str(e))
			response_code=500
	else:
		response_code=400

	return HttpResponse('something wrong')


def test(request):
	t=get_template('test.html')
	return HttpResponse(t.render())


class method(object):
	"""docstring for method"""
	def __init__(self, arg):
		super(method, self).__init__()
		self.arg = arg
	
	def func1(self):
		print('function 1 was called')

	def func2(self):
		print('function 2 was called')