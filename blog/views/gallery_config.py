import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse

from ..forms import ImageForm, GallerySearchForm
from ..models import ImageGallery, Image

@login_required(login_url='/blog/admin/login/')
def list_gallery(request):
	is_superauthor = request.user.groups.filter(name='superauthor').exists()
	if is_superauthor:
		model = ImageGallery
		name = 'Galleries'
		template = 'list_gallery.html'
		search_form = GallerySearchForm(request.GET)
		field_names = model.ViewMeta.table_columns
		data_all = model.objects.all()
		param={}
		if search_form.is_valid():
			data=search_form.cleaned_data
			date_from = data.get('date_from', None)
			date_till = data.get('date_till', None)
			if data.get('author'):
				param['created_by__iexact'] = data.get('author')
			if data.get('title'):
				param['title__icontains'] = data.get('title')
			if date_from:
				param['date__year__gte'] = date_from.year
				param['date__month__gte'] = date_from.month
				param['date__day__gte'] = date_from.day
			if date_till:
				param['date__year__lte'] = date_till.year
				param['date__month__lte'] = date_till.month
				param['date__day__lte'] = date_till.day

		if param:
			data_all = data_all.filter(**param)
			
		view_name = data_all.model.ViewMeta.view_name
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
		return render(request, template,{'paged_data': paged_data, 'view_name':view_name, 'name':name, 'fields':field_names, 
			'pages':pages_dict['pages'], 'pages_append':pages_dict['pages_append'], 'search_form':search_form})
	else:
		return HttpResponse(status=403)

@login_required(login_url='/blog/admin/login/')
def delete_gallery(request, galleryId):
	is_superauthor = request.user.groups.filter(name='superauthor').exists()
	if is_superauthor and request.is_ajax():
		model = ImageGallery
		try:
			data = ImageGallery.objects.get(id=galleryId)
			data.delete()
			return HttpResponse(json.dumps({'delete_status':'success'}))
		except:
			return HttpResponse(json.dumps({'delete_status':'failed'}))
	else:
		return HttpResponse(status=403)

def get_render(request, model, name, template='list_post.html'):
	field_names = model.ViewMeta.table_columns
	data_all = model.objects.all()
	view_name = data_all.model.ViewMeta.view_name
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
	return render(request, template,{'paged_data': paged_data, 'view_name':view_name, 'name':name, 'fields':field_names, 
		'pages':pages_dict['pages'], 'pages_append':pages_dict['pages_append']})

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
				imageId = submitted.id
				return HttpResponse(json.dumps({'upload_status':'success', 'file':fname, 'imageId':imageId}))
			else:
				return HttpResponse(json.dumps({'upload_status':formData.errors}))
		else:
			return HttpResponse(json.dumps({'message':'wrong method'}))
	else:
		return HttpResponse(json.dumps({'message':'wrong user'}))
@login_required(login_url='/blog/admin/login/')
def delete_image(request, id):
	is_superauthor = request.user.groups.filter(name='superauthor').exists()
	if is_superauthor and request.is_ajax():
		model = Image
		try:
			data = model.objects.get(id=galleryId)
			data.delete()
			return HttpResponse(json.dumps({'delete_status':'success'}))
		except:
			return HttpResponse(json.dumps({'delete_status':'failed'}))
	else:
		return HttpResponse(status=403)


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