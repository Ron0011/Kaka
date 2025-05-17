from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    path('adopt/', views.adopt, name='adopt'),
    path('add-pet/', views.add_pet, name='add_pet'),
    path('adopt/<int:pet_id>/', views.adopt_pet, name='adopt_pet'),
    path('delete-pet/<int:pet_id>/', views.delete_pet, name='delete_pet'),

    path('VeterinaryHospital/', views.veterinary_hospital_view, name='VeterinaryHospital'),
    path('book-vet-appointment/<int:hospital_id>/', views.book_vet_appointment, name='book_vet_appointment'),
    path('cancel-vet-booking/<int:booking_id>/', views.cancel_vet_booking, name='cancel_vet_booking'),
    path('manage_vet_bookings/', views.manage_vet_bookings, name='manage_vet_bookings'),

    path('petstore/', views.petstore, name='petstore'),
    path('place_order/<str:product_name>/', views.place_order, name='place_order'),
    path('add_to_cart/<str:product_name>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('remove_from_cart/<str:product_name>/', views.remove_from_cart, name='remove_from_cart'),
    path('order_success/', views.order_success, name='order_success'),
    path('payment_success/', views.payment_success, name='payment_success'),


    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('admin_manage_orders/', views.admin_manage_orders, name='admin_manage_orders'),
    path('my_orders/', views.my_orders, name='my_orders'),

]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
