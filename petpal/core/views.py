from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import UserProfile, Pet, Adoption, VetBooking, Order, Notification,VeterinaryHospital
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OrderForm
import razorpay
from django.conf import settings

def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        UserProfile.objects.create(user=user)
        messages.success(request, "Registration successful!")
        return redirect('login')
    return render(request, 'registration.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('home')

@login_required
def profile(request):
    pets_added = Pet.objects.filter(user=request.user)
    adoptions = Adoption.objects.filter(user=request.user)
    vet_bookings = VetBooking.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    
    context = {
        'pets_added': pets_added,
        'adoptions': adoptions,
        'vet_bookings': vet_bookings,
        'orders': orders,
        'notifications': notifications,
    }
    return render(request, 'profile.html', context)

@login_required
def adopt(request):
    pets = Pet.objects.all()
    return render(request, 'adopt.html', {'pets': pets})

@login_required
def add_pet(request):
    if request.method == 'POST':
        Pet.objects.create(
            user=request.user,
            name=request.POST['name'],
            breed=request.POST['breed'],
            age=request.POST['age'],
            image=request.FILES['image']
        )
        messages.success(request, "Pet added successfully!")
        return redirect('adopt')
    return redirect('adopt')

@login_required
def adopt_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if not pet.is_adopted:
        pet.is_adopted = True
        pet.save()
        Adoption.objects.create(user=request.user, pet=pet)
        if pet.user != request.user:
            Notification.objects.create(
                user=pet.user,
                message=f"Your pet '{pet.name}' was adopted by {request.user.username}!"
            )
    messages.success(request, "You have adopted a pet!")
    return redirect('adopt')

@login_required
def delete_pet(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)

    if pet.user == request.user:
        pet.delete()
        messages.success(request, "Pet removed successfully!")
    else:
        messages.error(request, "You cannot delete this pet!")

    return redirect('adopt')


@login_required
def veterinary_hospital_view(request):
    hospitals = VeterinaryHospital.objects.all()
    return render(request, 'vet.html', {'hospitals': hospitals})

@login_required
def book_vet_appointment(request, hospital_id):
    hospital = get_object_or_404(VeterinaryHospital, id=hospital_id)
    pets = Pet.objects.filter(user=request.user)

    if request.method == 'POST':
        pet_id = request.POST['pet']
        date = request.POST['date']
        time = request.POST['time']
        reason = request.POST['reason']

        pet = get_object_or_404(Pet, id=pet_id)
        VetBooking.objects.create(
            user=request.user,
            pet=pet,
            hospital=hospital,
            date=date,
            time=time,
            reason=reason
        )
        messages.success(request, "Vet appointment booked successfully!")
        return redirect('home') 

    return render(request, 'book_vet_appointment.html', {'hospital': hospital, 'pets': pets})

@login_required
def cancel_vet_booking(request, booking_id):
    booking = get_object_or_404(VetBooking, id=booking_id, user=request.user)
    booking.delete()
    messages.success(request, "Vet appointment cancelled successfully.")
    return redirect('profile')

@staff_member_required
def manage_vet_bookings(request):
    bookings = VetBooking.objects.all().order_by('-date')

    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        booking = get_object_or_404(VetBooking, id=booking_id)
        booking.status = new_status
        booking.save()
        messages.success(request, "Booking status updated successfully!")
        return redirect('manage_vet_bookings')

    return render(request, 'manage_vet_bookings.html', {'bookings': bookings})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def petstore(request):
    products = Product.objects.all()
    return render(request, 'petstore.html', {'products': products})

@login_required
def place_order(request, product_name):
    product = get_object_or_404(Product, name=product_name)
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_address = request.POST.get('customer_address')
        quantity = int(request.POST.get('quantity'))

        Order.objects.create(
            user=request.user,
            product_name=product.name,
            quantity=quantity,
            customer_name=customer_name,
            customer_phone=customer_phone,
            customer_address=customer_address,
        )
        messages.success(request, "Order placed successfully!")
        return redirect('petstore')

    return render(request, 'place_order.html', {'product': product})

@login_required
def add_to_cart(request, product_name):
    cart = request.session.get('cart', {})

    if product_name in cart:
        cart[product_name] += 1
    else:
        cart[product_name] = 1

    request.session['cart'] = cart
    messages.success(request, f"{product_name} added to cart.")
    return redirect('petstore')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('petstore')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_address = request.POST.get('customer_address')

        for product_name, quantity in cart.items():
            Order.objects.create(
                user=request.user,
                product_name=product_name,
                quantity=quantity,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_address=customer_address
            )
        
        request.session['cart'] = {}
        return redirect('order_success')

    return render(request, 'checkout.html')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_name, quantity in cart.items():
        price = get_product_price(product_name)
        item_total = price * quantity
        cart_items.append({
            'product_name': product_name,
            'quantity': quantity,
            'price': price,
            'item_total': item_total
        })
        total_price += item_total

    return render(request, 'view_cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

def get_product_price(product_name):
    prices = {
        'Pet botanics Training Reward bacon-Flavored Dog Treats': 5.99,
        'Oral B Dual Size Dog Toothbrush': 7.49,
        'PetArmor Plus Flea & Tick Prevention': 15.99,
        'Dog Toy Pack for Small Dogs': 9.99,
        'Drools Adult Chicken & Egg Dog Food': 12.99,
        'Jainsons Pet Products Combo Toy': 14.99,
    }
    return prices.get(product_name, 10.00)  

@login_required
def remove_from_cart(request, product_name):
    cart = request.session.get('cart', {})

    if product_name in cart:
        del cart[product_name]

    request.session['cart'] = cart
    messages.success(request, f"{product_name} removed from cart.")
    return redirect('view_cart')

def order_success(request):
    return render(request, 'order_success.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def payment_success(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "Your cart is empty!")
            return redirect('petstore')

        customer_name = request.session.get('customer_name')
        customer_phone = request.session.get('customer_phone')
        customer_address = request.session.get('customer_address')

        for product_name, quantity in cart.items():
            Order.objects.create(
                user=request.user,
                product_name=product_name,
                quantity=quantity,
                customer_name=customer_name,
                customer_phone=customer_phone,
                customer_address=customer_address,
                status='Paid'
            )

        request.session['cart'] = {}
        messages.success(request, "Payment successful! Order placed.")
        return redirect('order_success')

    return redirect('petstore')


def is_admin(user):
    return user.is_staff

def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid admin credentials.")
            return redirect('adminlogin')
    return render(request, 'adminlogin.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_users': UserProfile.objects.count(),
        'total_pets': Pet.objects.count(),
        'total_adoptions': Adoption.objects.count(),
        'total_vet_appointments': VetBooking.objects.count(),
        'total_orders': Order.objects.count(),
        'adoption_requests': Adoption.objects.all(),
        'vet_appointments': VetBooking.objects.all(),
    }
    return render(request, 'admin.html', context)

@login_required
@user_passes_test(is_admin)
def admin_logout(request):
    logout(request)
    return redirect('home')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty!")
        return redirect('petstore')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_address = request.POST.get('customer_address')

        total_price = 0
        for product_name, quantity in cart.items():
            total_price += get_product_price(product_name) * quantity

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': int(total_price * 100), 'currency': 'INR', 'payment_capture': '1'})

        request.session['payment_order_id'] = payment['id']
        request.session['customer_name'] = customer_name
        request.session['customer_phone'] = customer_phone
        request.session['customer_address'] = customer_address
        request.session['total_price'] = total_price

        return render(request, 'payment.html', {
            'payment': payment,
            'key_id': settings.RAZORPAY_KEY_ID,
            'total_price': total_price,
        })

    return render(request, 'checkout.html')

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_manage_orders(request):
    orders = Order.objects.all().order_by('-order_date')

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        new_status = request.POST.get('status')

        order = Order.objects.get(id=order_id)
        order.status = new_status
        order.save()
        messages.success(request, f"Order {order.id} status updated to {new_status}.")

        return redirect('admin_manage_orders')

    return render(request, 'admin_manage_orders.html', {'orders': orders})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'my_orders.html', {'orders': orders})

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Pet, Adoption, Order, VetBooking, User

@staff_member_required
def admin_dashboard(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')
        booking = VetBooking.objects.get(id=booking_id)
        booking.status = new_status
        booking.save()
        return redirect('admin_dashboard')

    context = {
        'total_users': User.objects.count(),
        'total_pets': Pet.objects.count(),
        'total_orders': Order.objects.count(),
        'total_vet_appointments': VetBooking.objects.count(),
        'adoption_requests': Adoption.objects.all().order_by('-adopted_at')[:5],
        'vet_appointments': VetBooking.objects.select_related('user', 'pet', 'hospital').order_by('-date')[:5],
    }
    return render(request, 'admin.html', context)
