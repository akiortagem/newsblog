from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(label='Username', max_length=100)
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
	username = forms.CharField(label='Username', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Username'}))
	password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
	first_name = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Nama Depan'}))
	last_name = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Nama Belakang'}))
	email = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Alamat Email'}))
	groups = forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple("Groups", is_stacked=False), queryset=Group.objects.all())
	#groups = forms.ModelChoiceField(Group.objects.all(), widget=FilteredSelectMultiple)

	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name', 'email', 'groups']
		
	class Media:
		css = {'all': ('/static/admin/css/widgets.css',),}
		js = ('/admin/jsi18n',)

class ChangePasswordForm(forms.Form):
	new_password = forms.CharField(label='Password', max_length=100, 
		widget=forms.PasswordInput(attrs={'placeholder':'masukkan password baru'}))
	new_password_repeat = forms.CharField(label='Password', max_length=100, 
		widget=forms.PasswordInput(attrs={'placeholder':'ulangi password baru'}))