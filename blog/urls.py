# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('create', views.create_blog, name='create_blog'),
    path('<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('<int:blog_id>/delete', views.delete_blog, name='delete_blog'),  # Add this line for the delete view

    # path('', views.blog_list, name='blog_list'),
]
