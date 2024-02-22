# appointment/urls.py
from django.urls import path
from . import views
app_name = 'appointment'  # Define the app namespace

urlpatterns = [
    path('doctor-list/', views.list_view, name='list_view'),
    path('confirmation/<int:appointment_id>/', views.confirmation_page, name='confirmation_page'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
]
