from django.shortcuts import render
from ..models import *
from django.contrib.auth.decorators import login_required

def index(request):
	model = Blog
	data_all = model.objects.all()
	posts = data_all[0:3]
	return render(request, 'index.html', {'posts':posts})

@login_required(login_url='/blog/admin/login/')
def dashboard(request):
	is_superuser = request.user.groups.filter(name='superuser').exists()
	return render(request, 'dashboard.html', {'is_superuser':is_superuser})