from django.contrib import admin
from .models import UserProfile, Pet, Adoption, Notification, VeterinaryHospital, VetBooking, Product, Order


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__username', 'phone_number')

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'breed', 'age', 'user', 'is_adopted')
    search_fields = ('name', 'breed', 'user__username')

@admin.register(Adoption)
class AdoptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'adopted_at')
    search_fields = ('user__username', 'pet__name')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    search_fields = ('user__username',)

@admin.register(VeterinaryHospital)
class VeterinaryHospitalAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'contact_number', 'email')
    search_fields = ('name', 'location')

@admin.register(VetBooking)
class VetBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'hospital', 'date', 'time', 'status')
    search_fields = ('user__username', 'pet__name', 'hospital__name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'product_name', 'quantity', 'customer_name', 'status', 'order_date')
    search_fields = ('user__username', 'product_name', 'customer_name')

