import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from ..forms import ImageForm
from ..models import ImageGallery, Image

@login_required(login_url='/blog/admin/login/')
def new_gallery(request):
	is_superauthor = request.user.groups.filter(name='superauthor').exists()
	if is_superauthor:
		form = ImageForm(initial={'uploaded_by':request.user.id})
		return render(request, 'new_gallery.html', {'form':form})

@login_required(login_url='/blog/admin/login/')
def upload_image(request):
	is_superauthor = request.user.groups.filter(name='superauthor').exists()
	if is_superauthor:
		form = ImageForm
		if request.method == "POST":
			formData = form(request.POST, request.FILES)
			if formData.is_valid():
				submitted = formData.save(commit=False)
				submitted.uploaded_by = request.user
				submitted.save()
				fname = str(submitted.image.name).split('/')[-1]
				return HttpResponse(json.dumps({'upload_status':'success', 'file':fname}))
			else:
				return HttpResponse(json.dumps({'upload_status':formData.errors}))
		else:
			return HttpResponse(json.dumps({'message':'wrong method'}))
	else:
		return HttpResponse(json.dumps({'message':'wrong user'}))		

@login_required(login_url='/blog/admin/login/')
def create_gallery(request):
	is_superauthor = request.user.groups.filter(name='superauthor').exists()
	if is_superauthor:
		if request.method == "POST":
			fns = request.POST.getlist('files[]')
			title = request.POST.get('title')
			gallery = ImageGallery()
			gallery.created_by = request.user
			gallery.title = title
			gallery.save()
			filenames = []
			images = []
			imagesName = []
			for filename in fns:
				filename = "media/" + filename
				image = Image.objects.get(image=filename)
				images.append(image)
				filenames.append(filename)
				imagesName.append(image.image.name)
			gallery.images.add(*images)
			try:
				gallery.save()
				return HttpResponse(json.dumps({'create_status':'success', 'title':title, 'files':filenames, 'images':imagesName}))
			except:
				return HttpResponse(json.dumps({'create_status':'failed', 'title':title, 'files':filenames, 'images':imagesName}))