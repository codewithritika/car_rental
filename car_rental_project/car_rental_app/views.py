from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail 
from django.contrib.auth.decorators import login_required

from car_rental_app.models import Booking, Car

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # change 'home' to your desired page
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. Please login.")
            return redirect('login')

    return render(request, 'register.html')


@login_required(login_url='login')
def home_view(request):
    cars = Car.objects.all()

    if request.method == 'POST':
        car_id = request.POST.get('car_id')
        rent_date = request.POST.get('rent_date')
        return_date = request.POST.get('return_date')

        if car_id and rent_date and return_date:
            car = Car.objects.get(id=car_id)
            Booking.objects.create(
                user=request.user,
                car=car,
                rent_date=rent_date,
                return_date=return_date
            )
            messages.success(request, f'You booked {car.title} from {rent_date} to {return_date}')

        return redirect('home')

    return render(request, 'home.html', {'cars': cars})
def car_detail_view(request, car_id):
    car = next((c for c in CARS if c['id'] == car_id), None)
    if not car:
        return render(request, '404.html', status=404)
    return render(request, 'car_detail.html', {'car': car})
CARS = [
    {
        'id': 1,
        'title': 'Luxury Sedan',
        'image': 'https://images.unsplash.com/photo-1642130204821-74126d1cb88e?q=80&w=1760&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'description': 'A premium sedan with luxury interior, smooth performance, and excellent mileage. KEY FEATURES:Body Style: 4 doors, fixed roof, and a separate boot (trunk).     Seating: Typically 5 passengers.   Ride Comfort: Smooth and stable ride, designed for comfort and long-distance travel. Handling: Offers better handling than larger vehicles.  Fuel Efficiency: Generally better than SUVs due to aerodynamic design.',},
    {
        'id': 2,
        'title': 'Electric Future',
        'image': "https://media.istockphoto.com/id/1477067152/photo/electric-car-power-charging.webp?a=1&b=1&s=612x612&w=0&k=20&c=Qb6NoEivbPGyf-YnRAEa6tfsZDWDwx6MSu0UCym3e9c=" ,
        'description': 'A cutting-edge electric car with zero emissions and futuristic design.',
    },
    {
        'id': 3,
        'title': 'Sports Beast',
        'image': 'https://images.unsplash.com/photo-1516298252535-cf2ac5147f9b?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8c3BvcnRzJTIwY2FyfGVufDB8fDB8fHww',
        'description': 'High-performance sports car built for speed and handling.',
    },
    {
        'id': 4,
        'title': 'Classic Muscle',
        'image': 'https://images.unsplash.com/photo-1489008777659-ad1fc8e07097?q=80&w=1740&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        'description': 'An iconic American muscle car with a roaring engine and vintage style.',
    },
]

 # optional, for sending email

def contact_view(request):
    success = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to database or send email — simplified here
        print(f'Contact message from {name} ({email}): {message}')
        success = True

        # Optional email heading (configure EMAIL settings in settings.py)
        # send_mail(
        #     subject=f"Message from {name}",
        #     message=message,
        #     from_email=email,
        #     recipient_list=['your@email.com']
        # )

    return render(request, 'contact.html', {'success': success})

# from .models import Booking

def admin_view(request):
    bookings = Booking.objects.select_related('user', 'car').all()
    return render(request, 'admin.html', {'bookings': bookings})
