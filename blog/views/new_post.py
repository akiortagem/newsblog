from django.shortcuts import render, redirect
from ..models import *
from ..forms import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/blog/admin/login/')
def edit_post(request, slug):
	return save_post(request, slug=slug)

@login_required(login_url='/blog/admin/login/')
def new_post(request):
	return save_post(request)

def save_post(request, slug=None):
	form = BlogForm
	if not slug:
		form_inst = form(initial={'author':request.user.id})
		mode='new'
	else:
		mode='edit'
		post = Blog.objects.get(slug=slug)
		if not post.author == request.user and not request.user.is_superuser:
			return HttpResponse(status=403)
		else:
			form_inst = form(instance=post)

	if request.method == 'POST':
		if not slug:
			formData = form(request.POST, request.FILES)
		else:
			formData = form(request.POST, request.FILES, instance=post)
		if formData.is_valid():
			if not slug:
				submitted = formData.save(commit=False)
				submitted.author = request.user
				submitted.save()
			else:
				formData.save()
			if 'add-another' in request.POST:
				return redirect('/blog/admin/post/new/'))
			else:
				return redirect('/blog/admin/post/list/')
		else:
			return render(request, 'post_status.html', {'status':'failed'})
	else:
		return render(request, 'new_post.html', {'form':form_inst, 'mode':mode})

@login_required(login_url='/blog/admin/login/')
def new_category(request):
	form = CategoryForm
	form_inst = form(initial={'author':request.user})
	if request.method == 'POST':
		formData = form(request.POST, request.FILES)
		if formData.is_valid():
			submitted = formData.save(commit=False)
			submitted.author = request.user
			submitted.save()
			if 'add-another' in request.POST:
				return render(request, 'new_post.html', {'form':form_inst})
			else:
				return render(request, 'post_status.html', {'status':'success'})
		else:
			return render(request, 'post_status.html', {'status':'failed'})
	else:
		return render(request, 'new_post.html', {'form':form_inst})

@login_required(login_url='/blog/admin/login/')
def edit_about_us(request):
	body = AboutUs.objects.all().first()
	form = AboutUsForm
	form_inst = AboutUsForm(instance=body) if body else AboutUsForm()
	if request.method == 'POST':
		formData = form(request.POST, request.FILES, instance=body) if body else form(request.POST, request.FILES) 
		if formData.is_valid():
			formData.save()
			return render(request, 'edit_about_us.html', {'status':'success'})
		else:
			return render(request, 'edit_about_us.html', {'status':'failed', 'form':form_inst})
	else:
		return render(request, 'edit_about_us.html', {'form':form_inst})