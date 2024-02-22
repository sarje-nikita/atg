from django.urls import path
from . import views
# from django.contrib import admin

app_name = 'account'

urlpatterns = [
    path('', views.index, name= 'index'),
    path('login', views.login_view, name='login_view'),
    path('register', views.register, name='register'),
    path('patient', views.patient, name='patient'),
    path('doctor', views.doctor, name='doctor'),
    path('logout_view', views.logout_view, name='logout_view'),
    path('home', views.home, name='home'),
    path('publish/<int:blog_id>', views.publish_draft, name='publish_draft'),
    path('blog_data/', views.blog_data, name='blog_data'),
    path('toggle_google_calendar', views.toggle_google_calendar, name='toggle_google_calendar'),

]