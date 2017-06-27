from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.show_info,name='show'),
	url(r'^req_form/',views.req_form,name='form'),
	url(r'^search/',views.search,name='search'),
	url(r'^tpl/',views.tpl,name='template'),
	url(r'^ocr/',views.ocr,name='ocr'),
	url(r'^test/',views.test,name='test'),
	url(r'^handle/',views.handle,name='handle'),
]