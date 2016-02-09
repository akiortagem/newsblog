from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blog import urls as blog_urls
from blog.views import view_index
urlpatterns = [
    # Examples:
    # url(r'^$', 'newsblog.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', view_index, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
