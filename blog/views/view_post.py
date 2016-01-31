import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.serializers.json import DjangoJSONEncoder
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
