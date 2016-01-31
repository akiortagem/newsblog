import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Q

from ..forms import LoginForm, ChangePasswordForm, UserForm
from . import dashboard
from . import index

def user_login(request):
	form = LoginForm
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponse(json.dumps({'login_status':'success'}))
			else:
				return HttpResponse(json.dumps({'login_status':'User tidak aktif'}))
		else:
			return HttpResponse(json.dumps({'login_status':'Username atau password anda salah'}))
	else:
		return render(request, 'login.html', {'form':form()})

def user_logout(request):
	logout(request)
	return redirect('../login/')



@login_required(login_url='/blog/admin/login/')
def change_password(request):
	form = ChangePasswordForm
	if request.method == 'POST':
		new_password = request.POST['new_password']
		new_password_repeat = request.POST['new_password_repeat']
		if new_password != new_password_repeat:
			return HttpResponse(json.dumps({'pass_status':'Password yang anda ketik tidak sama'}))
		user = request.user
		user.set_password(new_password)
		user.save()
		return HttpResponse(json.dumps({'pass_status':'success'}))
	else:
		return render(request, 'change_password.html', {'form':form()})

@login_required(login_url='/blog/admin/login/')
def user_add(request):
	is_superuser = request.user.groups.filter(name='superuser').exists()
	if is_superuser:
		form = UserForm
		group = Group.objects.get(name='Authors')
		if request.method == 'POST':
			formData = form(request.POST)
			if formData.is_valid():
				submitted = formData.save()
				submitted.groups.add(group)
				submitted.save()
				return HttpResponse(json.dumps({'user_status':'success'}))
			else:
				return HttpResponse(json.dumps({'user_status':'failed'}))
		else:
			return HttpResponse(json.dumps({'user_status':'only accepts POST'}))
	else:
		return HttpResponse(json.dumps({'user_status':'not superuser'}))

@login_required(login_url='/blog/admin/login/')
def user_delete(request, username):
	is_superuser = request.user.groups.filter(name='superuser').exists()
	if is_superuser:
		try:
			user = User.objects.get(username=username)
			user.delete()
			return HttpResponse(json.dumps({'user_status':'success'}))
		except:
			return HttpResponse(json.dumps({'user_status':'failed'}))
	else:
		return HttpResponse(json.dumps({'user_status':'not superuser'}))


@login_required(login_url='/blog/admin/login/')
def user_management(request):
	is_superuser = request.user.groups.filter(name='superuser').exists()
	if is_superuser:
		model = User
		name = 'User'
		form = UserForm
		return get_render(request, model, name, form, template='list_user.html')

def get_render(request, model, name, form, template='list_post.html'):
	data_all = model.objects.filter(~Q(username='admin'))
	limit = 10
	paginator = Paginator(data_all, limit)
	page = request.GET.get('page')
	try:
	  paged_data = paginator.page(page)
	  pages_dict = get_display_pages(page,limit, paginator.num_pages)
	except PageNotAnInteger:
	  paged_data = paginator.page(1)
	  pages_dict = get_display_pages(1, limit, paginator.num_pages)
	except EmptyPage:
	  paged_data = paginator.page(paginator.num_pages)
	  pages_dict = get_display_pages(paginator.num_pages, limit, paginator.num_pages)
	return render(request, template,{'paged_data': paged_data, 'name':name, 
		'pages':pages_dict['pages'], 'pages_append':pages_dict['pages_append'], 'form':form()})

def get_display_pages(page, limit, num_pages):
	page=int(page)
	if page > num_pages:
		page = num_pages

	if num_pages < 10:
		pages = range(1,num_pages)
		pages_append = [num_pages+1]
		return {'pages':pages, 'pages_append':pages_append}
		
	pages=[]
	pages_append=[]
	if page > limit:
		pages_append.append(1)
		start = page - ((page % 10) - 1 if page % 10 != 0 else 9)
		stop = start + 10
		for x in range(start, stop):
			if x <= num_pages:
				pages.append(x)
		pages_append.append(page-1)
		if x+1 <= num_pages:
			pages_append.append(x+1)
	elif page <= limit:
		for x in range(1,limit+1):
			pages.append(x)
		pages_append.append(x+1)
		
	return {'pages':pages, 'pages_append':pages_append}