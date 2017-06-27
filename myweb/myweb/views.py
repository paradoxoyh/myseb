from django.http import HttpResponse, StreamingHttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from show.models import Movie
import os


def hello(request):
	if request.session:
		print('there is a session object')
	return HttpResponse('Hello, this is your first Django program')


def firstpage(request):
	t=get_template('first_page.html')
	return HttpResponse(t.render())


def movie_info(request):
	Movies=Movie.objects.all()
	t=get_template('movie_info.html')
	c={'Movies':Movies}
	return HttpResponse(t.render(c))


def search_movie(request):
	Movies=Movie.objects.filter(year=request.GET['year']).order_by('point')
	if Movies:
		t=get_template('movie_info_year.html')
		c={'Movies':Movies,'year':request.GET['year'],'number':len(Movies)}
		return HttpResponse(t.render(c))
	else:
		return HttpResponse('invalid year input')


def video_info(request):
	t=get_template('video_info.html')
	path=os.getcwd()+'/Video'
	videos=os.listdir(path)
	c={'videos':videos}
	return HttpResponse(t.render(c))


def play(request,video_name):
	t=get_template('video_play.html')
	print(len(video_name))
	c={'video':video_name}
	return HttpResponse(t.render(c))


def file_info(request):
	t=get_template('file_info.html')
	path=os.getcwd()+'/download_src'
	files=os.listdir(path)
	c={'files':files}
	return HttpResponse(t.render(c))


def download(request,file_name):
	path=os.getcwd()+'/download_src/'+file_name
	if os.path.isfile(path):
		response=StreamingHttpResponse(file_iterator(path))
		response['Content-Type']='application/octet-stream'
		response['Content-Disposition']='attachment;filename="{0}"'.format(file_name)
		return response
	else:
		return HttpResponse('something wrong')


def file_iterator(file_name, chunk_size=512):
	with open(file_name,'rb') as f:
		while True:
			c=f.read(chunk_size)
			if c:
				yield c
			else:
				break