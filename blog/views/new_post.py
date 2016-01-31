from django.shortcuts import render
from ..models import *
from ..forms import *
from django.contrib.auth.decorators import login_required

@login_required(login_url='/blog/admin/login/')
def new_post(request):
	if not request.user.id:
		return render(request, '503.html')
	form = BlogForm
	form_inst = form(initial={'author':request.user.id})
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