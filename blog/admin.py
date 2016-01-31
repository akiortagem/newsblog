from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django import forms

from models import *

class BlogAdmin(admin.ModelAdmin):
	list_display = ('title','author', 'publish_on', 'status', 'slug')

class MessageAdmin(admin.ModelAdmin):
	list_display = ('name', 'phone', 'email', 'date', 'subject', 'status')

class ImageAdmin(admin.ModelAdmin):
	list_display = ('title', 'uploaded_by', 'date')

class ImageGalleryAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_by', 'date')
	filter_horizontal = ('images',)

admin.site.register(Blog, BlogAdmin)
admin.site.register(Category)
admin.site.register(Message, MessageAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(ImageGallery, ImageGalleryAdmin)
