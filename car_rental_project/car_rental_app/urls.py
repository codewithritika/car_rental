from django.urls import path

from car_rental_app import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('car/<int:car_id>/', views.car_detail_view, name='car_detail'),
    path('contact/', views.contact_view, name='contact'),
]