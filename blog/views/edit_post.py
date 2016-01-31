from django.shortcuts import render
from ..models import Blog
from ..forms import BlogForm

def edit_post(request, slug):
	form = BlogForm
	model = Blog
	post = Blog.objects.get(slug=slug)
	form_instance = form(instance=post)
	if request.method == 'POST':
		formData = form(request.POST, request.FILES, instance=post)
		if formData.is_valid():
			formData.save()
			if 'add-another' in request.POST:
				return render(request, 'new_post.html', {'form':form()})
			else:
				return render(request, 'post_status.html', {'form':form, 'status':'success'})
		else:
			return render(request, 'post_status.html', {'form':form, 'status':'failed'})
	else:
		return render(request, 'new_post.html', {'form':form_instance})