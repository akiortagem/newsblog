import json
from django.shortcuts import render, HttpResponse
from ..models import *
from ..forms import *
from django.contrib.auth.decorators import login_required

def insert_contact(request):
	form = MessageForm
	form_inst = form()
	if request.method == 'POST':
		formData = form(request.POST)
		if formData.is_valid():
			formData.save();
			return HttpResponse(json.dumps({'form_status':'success'}))
		else:
			return HttpResponse(json.dumps({'form_status':'failed'}))
	return render(request, 'contact.html',{'form':form_inst})
