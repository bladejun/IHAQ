from django.db import models
from datetime import datetime

# Create your models here.

class ChatNode(models.Model) :

	chat_unique_id = models.AutoField(primary_key=True)
	user_id = models.CharField(max_length=50, default="unknown")
	user_name = models.CharField(max_length=50, default="unknown")
	content = models.CharField(max_length=50, default="")
	class_id = models.CharField(max_length=50, default="")
	created_date = models.CharField(max_length=50,default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	ddabong = models.IntegerField(default=0)

	def __str__(self) :
		return self.content


class PDF(models.Model) :

	pdf_name = models.CharField(max_length=50, default="")
	pdf_url = models.CharField(max_length=50, default="")
	class_id = models.CharField(max_length=50, default="")
	pdf = models.FileField(default='', upload_to='pdfs/')

	def __str__(self) :
		return self.pdf_url


class ClassNode(models.Model) :

	class_name = models.CharField(max_length=50, default="")
	class_id = models.CharField(max_length=50, default="")
	founder_id = models.CharField(max_length=50, default="")
	founder_name = models.CharField(max_length=50, default="")
	created_date = models.CharField(max_length=50,default=datetime.now().strftime("%Y-%m-%d"))
	image = models.ImageField(upload_to='classImg/', default='classImg/LYAN1.jpg')
	number_of_user = models.IntegerField(default=0)
	user_list = models.TextField(default = '')

	def __str__(self) :
		return self.class_name


class Member(models.Model) :
	user_name = models.CharField(max_length=50, default= "")
	user_id = models.CharField(primary_key=True, max_length=50, default= "")
	user_psw = models.CharField(max_length=50, default = "")
	user_email = models.CharField(max_length=50, default= "")
	in_class_list = models.TextField(default = '')

	def __str__(self):
		return self.user_id




class Memo(models.Model) :

	user_id = models.CharField(primary_key=True, max_length=50, default= "")
	class_name = models.CharField(max_length=50, default="")
	class_id = models.CharField(max_length=50, default="")
	founder_id = models.CharField(max_length=50, default="")
	memo = models.TextField(default = '')


	def __str__(self) :
		return self.class_name + ',' + self.user_id