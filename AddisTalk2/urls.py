from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    
    # Blog URLs
    path('', include('blog.urls')),
    
    # Other apps
    path('about/', include('about.urls')),
    path('contact/', include('contact.urls')),
    
    # Authentication URLs
    path('accounts/', include('allauth.urls')),
]