from django import forms
from .models import Pet,VetBooking,Order

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'breed', 'age', 'image']


class VetBookingForm(forms.ModelForm):
    class Meta:
        model = VetBooking
        fields = ['pet', 'date', 'time', 'reason']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_address', 'quantity']

