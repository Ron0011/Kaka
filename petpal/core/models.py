from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    age = models.CharField(max_length=50)
    image = models.ImageField(upload_to='pets/')
    is_adopted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Adoption(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Person who adopted
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    adopted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} adopted {self.pet.name}"
        
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Receiver
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"

class VeterinaryHospital(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=300)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name


class VetBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    hospital = models.ForeignKey(VeterinaryHospital, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # NEW FIELD

    def __str__(self):
        return f"{self.pet.name} booking at {self.hospital.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    customer_address = models.TextField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Paid', 'Paid'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')],
        default='Pending'
    )
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)


