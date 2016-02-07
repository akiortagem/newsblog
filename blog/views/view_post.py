import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import *

def view_post(request, slug):
	model = Blog
	post = model.objects.get(slug=slug)
	latest_posts = model.objects.all()
	latest_posts = latest_posts[0:5]
	return render(request, 'view_post.html', {'post':post, 'latest_posts':latest_posts})

@login_required(login_url='/blog/admin/login/')
def view_message(request, id):
	if request.user.has_perm('blog.can_view_message'):
		model = Message
		data = model.objects.get(id=id)
		data.status = 'R'
		data.save()
		return HttpResponse(json.dumps({
			'from':data.name,
			'subject':data.subject,
			'email':data.email,
			'phone':data.phone,
			'date':data.date.isoformat(),
			'message':data.message
			}))
	return HttpResponse(json.dumps({'message':'invalid user'}))

def view_gallery(request, gallery_id):
	model = ImageGallery
	gallery = model.objects.get(id=gallery_id)
	return render(request, 'view_gallery.html', {'gallery':gallery})

def endless_images(request, gallery_id):
	model = ImageGallery
	gallery = model.objects.get(id=gallery_id)
	images_all = gallery.images.order_by('-date')
	limit = 2
	paginator = Paginator(images_all, limit)
	page = request.GET.get('page')
	try:
		images = paginator.page(page)
	except PageNotAnInteger:
		images = paginator.page(1)
	except EmptyPage:
		images = paginator.page(paginator.num_pages)
	return images_jsonizer(images)

def images_jsonizer(images):
	ajax_return = {
		'images':[],
		'paginator':{}	
	}
	queue = 1
	for image in images:
		ajax_image = {
			'image':image.name,
			'title':image.title,
			'caption':image.caption,
			'queue':queue
		}
		queue += 1
		ajax_return['images'].append(ajax_image)
	ajax_return['paginator']={
		'has_next':images.has_next(),
		'next':images.next_page_number() if images.has_next() else None
	}
	return HttpResponse(json.dumps(ajax_return))