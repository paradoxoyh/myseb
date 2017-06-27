"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.firstpage),   #首页界面
    url(r'^admin/', admin.site.urls,name='admin'),
    url(r'^hello/$',views.hello,name='hello'),
    url(r'^show/',include('show.urls',namespace='show')),
    url(r'^movie/$',views.movie_info,name='movie'),
    url(r'^movie/search/$',views.search_movie,name='search'),
    url(r'^file_info/$',views.file_info,name='file'),
    url(r'^download/(?P<file_name>.*)$',views.download,name='download'),
    url(r'^video_info/$',views.video_info,name='video'),
    url(r'^video_play/(?P<video_name>.*)$',views.play,name='play'),
]
