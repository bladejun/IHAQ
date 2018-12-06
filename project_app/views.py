from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.core import serializers
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
import random, string
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
import smtplib
from email.mime.text import MIMEText
from django.template import loader
from .forms import ClassNodeForm
from .models import ClassNode

# Create your views here.
def index(request) :

	pdfs = PDF.objects.filter(class_id = 'A')

	context = { 'pdfs' : pdfs }

	return render(request, './chat+viewer.html', context)



def cc_test(request) :

	return render(request, './create_class.html')


def joinClass(request) :

	if request.method == 'GET' :

		#print(request.path.split('/')[2])

		class_id = request.path.split('/')[2]

		#print(class_id)

		classnode = ClassNode.objects.get(class_id = class_id)

		pdfs = PDF.objects.filter(class_id = class_id)

		if not request.session.get('login_complete', False):

			N = 8
			random_unique_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N));

			user_list = []
			for item in classnode.user_list.split(',') :
			    if '[' in item :
			        item = item.replace('[', '')
			    if '\'' in item :
			        item = item.replace('\'', '')
			    if ']' in item :
			        item = item.replace(']', '')
			    user_list.append(item.strip())

			while True :
				if random_unique_id in user_list :
					random_unique_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N));
				else :
					user_info = random_unique_id + '(unknown)'
					if user_info not in user_list :
						user_list.append(user_info)
					if '.' in user_list :
						user_list.remove('.')

					if '' in user_list :
						user_list.remove('')
					#print(user_list)
					classnode.user_list = user_list
					classnode.save()
					break
            
			unknown_member = Member(user_name = 'unknown', user_id = random_unique_id)

			context = { 'member' : unknown_member ,  'pdfs' : pdfs , 'classnode' : classnode }

		else :

			user_id = request.session.get('user_id', 'unknown')
			user_name = request.session.get('user_name', 'unknown')

			try :
				this_member = Member.objects.get(user_id = user_id)
				in_class_list = []
				for item in this_member.in_class_list.split(',') :
				    if '[' in item :
				        item = item.replace('[', '')
				    if '\'' in item :
				        item = item.replace('\'', '')
				    if ']' in item :
				        item = item.replace(']', '')
				    in_class_list.append(item.strip())

				if class_id not in in_class_list :
					in_class_list.append(class_id)
				if '.' in in_class_list :
					in_class_list.remove('.')
				if '' in in_class_list :
					in_class_list.remove('')

				this_member.in_class_list = in_class_list
				this_member.save()

			except :
				pass

			member = Member(user_name = user_name, user_id = user_id)

			try :
				memo = Memo.objects.get(class_id = class_id, user_id = user_id)
				context = { 'member' : member ,  'pdfs' : pdfs  , 'classnode' : classnode , 'memo' : memo}
			except :
				context = { 'member' : member ,  'pdfs' : pdfs  , 'classnode' : classnode }

			#print(context)

			#print(user_id)

			"""
			classnode = ClassNode.objects.get(class_id = class_id)
			classnode.number_of_user = classnode.number_of_user + 1
			classnode.save()
			"""


			user_list = []
			for item in classnode.user_list.split(',') :
			    if '[' in item :
			        item = item.replace('[', '')
			    if '\'' in item :
			        item = item.replace('\'', '')
			    if ']' in item :
			        item = item.replace(']', '')
			    user_list.append(item.strip())


			user_info = user_id + "(" + user_name + ")"
			if user_info not in user_list :
				user_list.append(user_info)
			if '.' in user_list :
				user_list.remove('.')

			if '' in user_list :
				user_list.remove('')
			classnode.user_list = user_list
			classnode.save()



		return render(request, './chat+viewer.html', context)

	# PDF 등록
	if request.method == 'POST':
		class_id = request.POST.get('class_id_text', False)

		for pdf in request.FILES.getlist('upload[]'):
			#print(pdf)
			print(class_id, pdf.name)
			pdf_url = "../media/pdfs/" + "[" + class_id + "]" + pdf.name
			new_pdf = PDF(pdf_name = "[" + class_id + "]" + pdf.name,
				pdf_url = pdf_url, 
				class_id = class_id, 
				pdf = pdf)
			#print(new_pdf)
			new_pdf.save()
			#fs = FileSystemStorage()
			#filename = fs.save(pdf.name, pdf)
			#uploaded_file_url = fs.url(filename)
			#print(uploaded_file_url)

		#print(request.POST.get('class_id_text', False))

		pdfs = PDF.objects.filter(class_id = class_id)

		context = { 'pdfs' : pdfs }

		"""
		file_get = request.POST.get('upload', False)
		if(file_get == False) :
			img_src = request.FILES['upload']
			fs = FileSystemStorage()
			filename = fs.save(img_src.name, img_src)
		"""

		return render(request, './chat+viewer.html', context)



def main(request) :

	if request.method == 'GET' :

		if not request.session.get('login_complete', False):
			unknown_member = Member(user_name='unknown', user_id = 'unknown')
			context = { 'member' : unknown_member }

		else :
			user_id = request.session.get('user_id', 'unknown')
			user_name = request.session.get('user_name', 'unknown')

			member = Member(user_name=user_name, user_id = user_id)

			context = { 'member' : member }

		return render(request, './main.html', context)

	if request.method == 'POST':

		user_name=request.POST['user_name']
		#user_name = request.POST.get('user_name', False);
		user_id = request.POST['user_id']
		user_psw = request.POST['user_psw']
		#user_email = request.POST.get('user_email', False);
		user_email=request.POST['user_email']

		new_member = Member(user_name=user_name, user_id = user_id, user_psw = user_psw, user_email=user_email)
		#멤버 객체 생성 
		new_member.save()

		context = { 'member' : new_member }

		request.session['login_complete'] = True
		request.session['user_id'] = user_id
		request.session['user_name'] = user_name

		return render(request, './main.html', context)


def logout(request) :

	request.session['login_complete'] = False

	unknown_member = Member(user_name='unknown', user_id = 'unknown')

	context = { 'member' : unknown_member }

	return render(request, './main.html', context)


def check_login(request) :

	user_id = request.GET.get('id',None)
	user_psw = request.GET.get('psw',None)

	try :
		member = Member.objects.get(user_id = user_id)
		#print(user_id, user_psw, member)
		if member.user_psw != user_psw :
			result = { "result" : "psw_failed"}
		else :
			request.session['login_complete'] = True
			request.session['user_id'] = user_id
			request.session['user_name'] = member.user_name

			result = { "result" : "success" }

	except :
		result = { "result" : "id_failed" }
		
	#print(result)
	return JsonResponse(result)


def login(request) :

	user_id = request.session.get('user_id', False)
	user_name = request.session.get('user_name', False)

	#print(user_id, user_name)
	member = Member.objects.get(user_id = user_id)

	#member = Member(user_name=user_name, user_id = user_id)

	#context = { 'member' : member }

	#return render(request, './main.html', context)

	return redirect('../main/')


def register(request) :

	return render(request, './register.html')


"""
def pdf_upload(request) :

	if request.method == 'POST':
		for f in request.FILES.getlist('upload[]'):
			print(f)

		#print(request.POST.get('class_id_text', False))

		class_id = request.POST.get('class_id_text', False)
		pdfs = PDF.objects.filter(class_id = class_id)

		context = { 'pdfs' : pdfs }

		return render(request, './chat+viewer.html', context)
		#return redirect(request, './chat+viewer.html', context)
"""


def check_class(request) :

	try :
		class_id = request.GET.get('class_id',None)

		classnode = ClassNode.objects.get(class_id = class_id)
		result = { "result" : "success"}

	except :

		result = { "result" : "failed"}


	return JsonResponse(result)







def inputClass(request) :

	return render(request, './input_class.html')



def create_class(request) :

	if request.method == 'GET' :

		class_name = request.GET.get('class_name',None)
		class_code = request.GET.get('class_code',None)
	
		result = { "result" : "success" }

		print(class_name, class_code)

		new_class = ClassNode(class_name = class_name, class_code = class_code)
		new_class.save()

		return JsonResponse(result)

def pdf(request) :

	return render(request, './viewer_test.html')


def updateChat(request) :

	if request.method == 'GET' :

		class_id = request.GET.get('class_id',None)

		json_serializer = serializers.get_serializer("json")()
		#chats = json_serializer.serialize(ChatNode.objects.filter(class_id=class_id).order_by('ddabong').reverse(), ensure_ascii=False)
		chats = json_serializer.serialize(ChatNode.objects.filter(class_id=class_id), ensure_ascii=False)
		#chats = json_serializer.serialize(Chat.objects.all(), ensure_ascii=False)
		#chats = Chat.objects.all()

		try :
			class_user_list = ClassNode.objects.get(class_id = class_id).user_list
		except :
			class_user_list = []
	
		result = { "chats" : chats , "class_user_list" : class_user_list }

		#print(result)

		return JsonResponse(result)


def sendChat(request) :

	if request.method == 'GET' :

		now = datetime.now()
		#print(now)

		user_id = request.GET.get('user_id',None)
		user_name = request.GET.get('user_name',None)
		chat_content = request.GET.get('chat_content',None)
		class_id = request.GET.get('class_id',None)

		#print(chat_content)

		new_chat = ChatNode(user_id = user_id, user_name = user_name, content = chat_content, class_id = class_id)
		new_chat.save()
	
		result = { "result" : 'false' }

		return JsonResponse(result)


def ddabong(request) :

	if request.method == 'GET' :

		user_name = request.GET.get('user_name',None)
		content = request.GET.get('content',None)
		class_id = request.GET.get('class_id',None)
		date = request.GET.get('date',None)
		is_ddabong = request.GET.get('is_ddabong',None)

		print(user_name, content, class_id, date, is_ddabong)

		if is_ddabong == 'no' :
			chat = ChatNode.objects.get(user_name = user_name, content = content, class_id=class_id, created_date = date)
			#print(chat.ddabong)
			chat.ddabong = chat.ddabong + 1
			chat.save()
		elif is_ddabong == 'yes' :
			chat = ChatNode.objects.get(user_name = user_name, content = content, class_id=class_id, created_date = date)
			#print(chat.ddabong)
			chat.ddabong = chat.ddabong - 1
			chat.save()
	
		result = { "result" : 'false' }

		return JsonResponse(result)


def delete_msg(request) :

	if request.method == 'GET' :

		user_name = request.GET.get('user_name',None)
		content = request.GET.get('content',None)
		class_id = request.GET.get('class_id',None)
		date = request.GET.get('date',None)

		print(user_name, content, class_id, date)

		chat = ChatNode.objects.get(user_name = user_name, content = content, class_id=class_id, created_date = date)
		#print(chat.ddabong)
		#chat.ddabong = chat.ddabong + 1
		chat.delete()
	
		result = { "result" : 'false' }

		return JsonResponse(result)




def join(request) :

	members = Member.objects.all()
	context = {'members' : members}
	return render(request, './join.html', context)

def check_id(request):

	if request.method == 'GET' :
		print(request.GET.get('user_id',None))
		user_id = request.GET.get('user_id',None)

		try:
			member_list = Member.objects.get(user_id = user_id)
			result = {"result" : 'true'}
		except :
			result = {"result" : 'false'}

	return JsonResponse(result)


def register_member_db(request):

	if request.method == 'POST':

		user_name=request.POST['user_name']
		#user_name = request.POST.get('user_name', False);
		user_id = request.POST['user_id']
		user_psw = request.POST['user_psw']
		#user_email = request.POST.get('user_email', False);
		user_email=request.POST['user_email']

		new_member = Member(user_name=user_name, user_id = user_id, user_psw = user_psw, user_email=user_email)
		#멤버 객체 생성 
		new_member.save()

		return render(request, './main.html')


def check_set_name(request) :

	user_name = request.GET.get('user_name',None)

	member_list = Member.objects.filter(user_name = user_name)
	if member_list :
		result = { "result" : "failed" }
	else :
		result = { "result" : "success" }

	return JsonResponse(result)


def save_memo(request) :

	class_id = request.GET.get('class_id',None)
	class_name = request.GET.get('class_name',None)
	user_id = request.GET.get('user_id',None)
	founder_id = request.GET.get('founder_id',None)
	memo = request.GET.get('memo',None)

	try :
		memonode = Memo.objects.get(class_id = class_id, class_name = class_name, user_id = user_id, founder_id = founder_id)
		memonode.memo = memo
		memonode.save()

	except :
		new_memo = Memo(class_id = class_id, class_name = class_name, user_id = user_id, founder_id = founder_id, memo = memo)
		new_memo.save()

	result = { "result" : "success" }

	return JsonResponse(result)

from django.core.mail import EmailMessage

def send_email_test(request) :

	#email = EmailMessage('subject text', 'body text', to=['wnstlr24@naver.com'])
	#email.send()

	return render(request, './main.html')


def delte_user_list(request) :

	class_id = request.GET.get('class_id',None)
	user_id = request.GET.get('user_id',None)
	user_name = request.GET.get('user_name',None)
	#print(class_id)

	classnode = ClassNode.objects.get(class_id = class_id)

	user_list = []
	for item in classnode.user_list.split(',') :
	    if '[' in item :
	        item = item.replace('[', '')
	    if '\'' in item :
	        item = item.replace('\'', '')
	    if ']' in item :
	        item = item.replace(']', '')
	    user_list.append(item.strip())

	user_info = user_id + "(" + user_name + ")"
	if user_info in user_list :
		user_list.remove(user_info)

	classnode.user_list = user_list
	classnode.save()

	result = { "result" : "success" }

	return JsonResponse(result)


def get_in_class_list(request) :

	user_id = request.session.get('user_id', 'unknown')
	member = Member.objects.get(user_id = user_id)

	classnodes = ClassNode.objects.filter(founder_id = user_id)

	in_class_lists = []
	for item in member.in_class_list.split(',') :
	    if '[' in item :
	        item = item.replace('[', '')
	    if '\'' in item :
	        item = item.replace('\'', '')
	    if ']' in item :
	        item = item.replace(']', '')
	    in_class_lists.append(item.strip())


	context = { "member" : member , "in_class_lists" : in_class_lists}

	return render(request, './get_in_class_list.html', context)



def delete_pdf(request) :

	if request.method == 'GET' :

		pdf_url = request.GET.get('pdf_url', None)
		class_id = request.GET.get('class_id', None)

		print(pdf_url)

		pdf_url_lst = pdf_url.split('/')

		url = "../" + pdf_url_lst[1] + "/" + pdf_url_lst[2] + "/" + "[" + class_id + "]" + pdf_url_lst[3]
		print(url)

		#pdf = PDF.objects.get(pdf_url = url)
		#pdf.delete()

		
		pdfs = PDF.objects.filter(class_id = class_id)
		for item in pdfs :
			#print(item.pdf.url)
			if item.pdf.url == pdf_url :
				#print(pdf_url)
				item.delete()
		

		#pdfs = PDF.objects.filter(class_id = class_id)

		#context = { 'pdfs' : pdfs }

		"""
		file_get = request.POST.get('upload', False)
		if(file_get == False) :
			img_src = request.FILES['upload']
			fs = FileSystemStorage()
			filename = fs.save(img_src.name, img_src)
		"""

		result = { "result" : "success" }

		return JsonResponse(result)
def password_change(request) :
	return render(request, './password_change.html')


def check_validation(request) : 

	user_id = request.GET.get('id',None)
	user_email = request.GET.get('email',None)

	try :
		member = Member.objects.get(user_id = user_id)
		#print(user_id, user_psw, member)
		if member.user_email != user_email :
			result = { "result" : "email_failed"}
		else :
			#request.session['validation'] = True
			request.session['user_id'] = user_id
			request.session['user_email'] = user_email

			result = { "result" : "success" }

	except :
		result = { "result" : "id_failed" }
		
	#print(result)
	return JsonResponse(result)

def password_change_success(request) :
	if request.method == 'POST':
		user_email = request.POST.get('email',None)
		user_id = request.POST.get('id',None)

		print(user_email)
		send_mail(
		'Password_Reset',
		'http://localhost:8000/password_validation_check/'+user_id ,
		'tlsjh082@gmail.com',
		[user_email],
		fail_silently=False,
		)
		return render(request, './password_change_success.html')


def password_validation_check(request): 
	#print(request.path.split('/')[2])
	id = request.path.split('/')[2]
	member = Member.objects.get(user_id = id)
	return render(request, './password_validation_check.html', {'member':member})

def psw_changed_success(request):
	if request.method == 'POST':
		id = request.path.split('/')[2]
		member = Member.objects.get(user_id = id)
		user_psw=request.POST.get('user_psw',False)
		member.user_psw=user_psw
		member.save()
		return render(request, './psw_changed_success.html')
 
def mypage(request):
 	user_id = request.session.get('user_id', False)
 	myself = Member.objects.filter(user_id = user_id)
 	classMake_check = ClassNode.objects.filter(founder_id = user_id)
 	classConnect_check = Member.objects.filter(user_id = user_id).values('in_class_list')

 	con_list = []
 	for item in classConnect_check[0]['in_class_list'].split(','):
 		if '[' in item :
 			item = item.replace('[', '')
 		if '\'' in item :
 			item = item.replace('\'', '')
 		if ']' in item :
 			item = item.replace(']', '')
 		con_list.append(item.strip())
	
 	classConnect_len = len(con_list)
 	classMake_count = classMake_check.count()

 	classimages1 = ClassNode.objects.filter(founder_id = 'default')
 	classimages2 = ClassNode.objects.filter(founder_id = 'default')
 	classimages3 = ClassNode.objects.filter(founder_id = 'default')
 	classimages4 = ClassNode.objects.filter(founder_id = 'default')

 	if classMake_count > 1:
 		classimages1 = ClassNode.objects.filter(founder_id = user_id)[classMake_check.count()-2:classMake_check.count()-1]
 		classimages2 = ClassNode.objects.filter(founder_id = user_id)[classMake_check.count()-1:classMake_check.count()]
 	if classMake_count == 1:
 		classimages1 = ClassNode.objects.filter(founder_id = user_id)[classMake_check.count()-1:classMake_check.count()]

 	if classConnect_len > 0 and len(con_list[0]) > 0:
 		classimages3 = ClassNode.objects.filter(class_id = con_list[len(con_list)-2])
 		if classConnect_len > 1:
 			classimages4 = ClassNode.objects.filter(class_id = con_list[len(con_list)-1])
		
 	return render(request, 'my_page.html', {
 		'myself' : myself , 'classimages1' : classimages1, 'classimages2' : classimages2,
 		'classimages3' : classimages3, 'classimages4' : classimages4,
 	})			
	
def upload_class(request):
 	user_id = request.session.get('user_id', False)
 	myself = Member.objects.filter(user_id = user_id)

 	if request.method == 'POST':
 		form = ClassNodeForm(request.POST, request.FILES)
 		if form.is_valid():
 			form.save()
 			return redirect('../')
 	else:
 		form = ClassNodeForm()
 		return render(request, 'upload_class.html', {
 		'form':form, 'myself' : myself
 		})	

 	