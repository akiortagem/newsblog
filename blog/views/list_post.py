import json
from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from ..models import *
from ..forms import MessageSearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from django.db.models import ForeignKey
from django.contrib.auth.decorators import login_required, user_passes_test

@login_required(login_url='/blog/admin/login/')
def list_post(request):
	model = Blog
	name = 'Posts'
	return get_render(request, model, name)

@login_required(login_url='/blog/admin/login/')
def list_message(request):
	if request.user.has_perm('blog.can_view_message'):
		template = 'list_message.html'
		model = Message
		name = 'Messages'
		search_form = MessageSearchForm(request.GET)
		field_names = model.ViewMeta.table_columns
		data_all = model.objects.all()
		param={}
		if search_form.is_valid():
			data=search_form.cleaned_data
			date_from = data.get('date_from', None)
			date_till = data.get('date_till', None)
			if data.get('name'):
				param['name'] = data.get('name')
			if data.get('email'):
				param['email'] = data.get('email')
			if data.get('subject'):
				param['subject'] = data.get('subject')
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
	return render(request, 'list_message.html',{'context':'you cannot view this page'})

@login_required(login_url='/blog/admin/login/')
def count_unreads(request):
	if request.user.has_perm('blog.can_view_message'):
		messages = Message.objects.filter(status='UR')
		unreads = len(messages)
		return HttpResponse(json.dumps({'unreads':unreads}))


def list_post_front(request, template='list_post_front.html'):
	return render(request, template)

def endless_post(request):
	model = Blog
	name = 'Posts'
	post_all = model.objects.all()
	limit = 2
	paginator = Paginator(post_all, limit)
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	return jsonizer_post(posts)

def jsonizer_post(posts):
	ajax_return = {
		'posts':[],
		'paginator':{}	
	}
	for post in posts:
		ajax_post = {
			'picture':post.picture.name,
			'slug':post.slug,
			'title':post.title,
			'posted':post.posted.strftime('%d %b %Y %H:%M:%S'),
			'body':post.body_shortened
		}
		ajax_return['posts'].append(ajax_post)
	ajax_return['paginator']={
		'has_next':posts.has_next(),
		'next':posts.next_page_number() if posts.has_next() else None
	}
	return HttpResponse(json.dumps(ajax_return))


def list_gallery_front(request, page_template='gallery_pagination.html', template='list_gallery_front.html'):
	return render(request, template)

def endless_gallery(request):
	model = ImageGallery
	gallery_all = model.objects.all()
	limit = 2
	paginator = Paginator(gallery_all, limit)
	page = request.GET.get('page')
	try:
		galleries = paginator.page(page)
	except PageNotAnInteger:
		galleries = paginator.page(1)
	except EmptyPage:
		galleries = paginator.page(paginator.num_pages)
	return jsonizer_gallery(galleries)

def jsonizer_gallery(galleries):
	ajax_return = {
		'galleries':[],
		'paginator':{}	
	}
	for gallery in galleries:
		ajax_gallery = {
			'first_pic':gallery.images.first().image.name,
			'id':gallery.id,
			'title':gallery.title,
		}
		ajax_return['galleries'].append(ajax_gallery)
	ajax_return['paginator']={
		'has_next':galleries.has_next(),
		'next':galleries.next_page_number() if galleries.has_next() else None
	}
	return HttpResponse(json.dumps(ajax_return))

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