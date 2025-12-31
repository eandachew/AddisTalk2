from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_view, name='contact'),
    # Remove any other paths, especially 'messages/' line
]