from django import forms
from django.forms.extras.widgets import SelectDateWidget
from custom_widgets import *

from ..models import *

class BlogForm(forms.ModelForm):
	category = forms.ModelChoiceField(Category.objects.all(),
			required=True,
			widget=SelectWithPlus
			)

	publish_on = forms.DateField(widget=SelectDateWidget)

	class Meta:
		model = Blog
		exclude = ['posted', 'author']

class MessageForm(forms.ModelForm):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
	phone = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'No Telepon'}))
	email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Alamat E-Mail'}))
	subject = forms.CharField(max_length=140, widget=forms.TextInput(attrs={'placeholder': 'Perihal'}))
	message = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'placeholder': 'Pesan Anda'}))

	class Meta:
		model = Message
		exclude = ['date', 'status']

class MessageSearchForm(forms.Form):
	name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Dari'}), required=False)
	subject = forms.CharField(max_length=140, widget=forms.TextInput(attrs={'placeholder': 'Perihal'}), required=False)
	email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Alamat E-Mail'}), required=False)

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		exclude = ['author']

class ImageForm(forms.ModelForm):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Judul'}))
	caption = forms.CharField(max_length=140, widget=forms.TextInput(attrs={'placeholder': 'Penjelasan/Kata-kata singkat'}))

	class Meta:
		model = Image
		exclude = ['date', 'uplodaded_by']
