from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^view/(?P<slug>[-\w]+)/', views.view_post, name='view_post'),
	url(r'^posts/get/',views.endless_post, name='endless_post'),
	url(r'^posts/',views.list_post_front, name='list_post_front'),
	url(r'^contact/',views.insert_contact, name='contact'),
	url(r'^gallery/',views.list_gallery_front, name='list_gallery_front'),
	url(r'^admin/message/count_unread',views.count_unreads, name='count_unreads'),
	url(r'^admin/message/(?P<id>[-\w]+)',views.view_message, name='view_message'),
	url(r'^admin/message/',views.list_message, name='list_message'),
	url(r'^admin/post/edit/(?P<slug>[-\w]+)/',views.edit_post, name='edit_post'),
	url(r'^admin/post/new/',views.new_post, name='new_post'),
	url(r'^admin/category/new/',views.new_category, name='new_category'),
	url(r'^admin/post/list/',views.list_post, name='list_post'),
	url(r'^admin/login/', views.user_login, name='user_login'),
	url(r'^admin/logout/', views.user_logout, name='user_logout'),
	url(r'^admin/change_password/', views.change_password, name='change_password'),
	url(r'^admin/user_management/user_add/', views.user_add, name='user_add'),
	url(r'^admin/user_management/user_delete/(?P<username>[-\w]+)/', views.user_delete, name='user_delete'),
	url(r'^admin/user_management/', views.user_management, name='user_management'),
	url(r'^admin/gallery/new/create/', views.create_gallery, name='create_gallery'),
	url(r'^admin/gallery/new/upload_image/', views.upload_image, name='upload_image'),
	url(r'^admin/gallery/new/', views.new_gallery, name='new_gallery'),
	url(r'^admin/dash/', views.dashboard, name='dashboard'),
    url(r'^', views.index, name='view_index'),
]