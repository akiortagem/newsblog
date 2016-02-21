from django.shortcuts import render, HttpResponse
from ..models import Blog
from ..forms import BlogForm

def edit_post(request, slug):
	if request.user.has_perm('blog.can_change_blog'):
		form = BlogForm
		model = Blog
		post = Blog.objects.get(slug=slug)
		if not post.author == request.user and not request.user.is_superuser:
			return HttpResponse(status=403)

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
	else:
		return HttpResponse(status=403)