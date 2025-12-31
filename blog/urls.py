from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('post/<slug:slug>/comment/<int:comment_id>/edit/', views.comment_edit, name='comment_edit'),
    path('post/<slug:slug>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('post/<slug:slug>/like/', views.post_like, name='post_like'),
]