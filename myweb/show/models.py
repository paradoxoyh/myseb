from django.db import models

# Create your models here.
class Movie(models.Model):
	"""docstring for movies"""
	name=models.CharField(max_length=20)
	year=models.IntegerField()
	director=models.CharField(max_length=20)
	point=models.FloatField()
	count_point=models.IntegerField()
	website=models.URLField() #日后再添加功能
	
	def __str__(self):
		return self.name

'''
class Y(models.Model):
	"""docstring for year"""
	movie=models.ForeignKey(Movie)

	def __str__(self):
		return self.name
'''
		