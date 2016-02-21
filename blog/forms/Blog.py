from django import forms
from django.forms.extras.widgets import SelectDateWidget
from custom_widgets import *
from tinymce.widgets import TinyMCE

from ..models import *

class BlogForm(forms.ModelForm):
	category = forms.ModelChoiceField(Category.objects.all(),
			required=True,
			widget=SelectWithPlus
			)

	publish_on = forms.DateField(widget=SelectDateWidget)
	body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

	class Meta:
		model = Blog
		exclude = ['posted', 'author']

class BlogSearchForm(forms.Form):
	category = forms.ModelChoiceField(Category.objects.all(), widget=forms.Select, required=False)
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Judul'}), required=False)
	author = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Penulis'}), required=False)
	date_from = forms.DateTimeField(
		required=False,
		input_formats=['%Y-%m-%d'],
		label='Dari Tanggal'
		)
	date_till = forms.DateTimeField(
		required=False,
		input_formats=['%Y-%m-%d'],
		label='Hingga Tanggal'
		)

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
	date_from = forms.DateTimeField(
		required=False,
		input_formats=['%Y-%m-%d'],
		label='Dari Tanggal'
		)
	date_till = forms.DateTimeField(
		required=False,
		input_formats=['%Y-%m-%d'],
		label='Hingga Tanggal'
		)

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

class GallerySearchForm(forms.Form):
	title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Judul'}), required=False)
	author = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Dibuat oleh'}), required=False)
	date_from = forms.DateTimeField(
		required=False,
		input_formats=['%Y-%m-%d'],
		label='Dari Tanggal'
		)
	date_till = forms.DateTimeField(
		required=False,
		input_formats=['%Y-%m-%d'],
		label='Hingga Tanggal'
		)

class AboutUsForm(forms.ModelForm):

	body = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

	class Meta:
		model = AboutUs
		exclude = ['date']