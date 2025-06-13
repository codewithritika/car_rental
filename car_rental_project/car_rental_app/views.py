from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail 

from car_rental_app.models import Car

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

from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home_view(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': CARS})

def car_detail_view(request, car_id):
    car = next((c for c in CARS if c['id'] == car_id), None)
    if not car:
        return render(request, '404.html', status=404)
    return render(request, 'car_detail.html', {'car': car})
CARS = [
    {
        'id': 1,
        'title': 'Luxury Sedan',
        'image': 'https://cdn.pixabay.com/photo/2017/01/06/19/15/auto-1957037_1280.jpg',
        'description': 'A premium sedan with luxury interior, smooth performance, and excellent mileage.',
    },
    {
        'id': 2,
        'title': 'Electric Future',
        'image': 'https://cdn.pixabay.com/photo/2020/06/12/15/48/car-5288361_1280.jpg',
        'description': 'A cutting-edge electric car with zero emissions and futuristic design.',
    },
    {
        'id': 3,
        'title': 'Sports Beast',
        'image': 'https://cdn.pixabay.com/photo/2016/03/27/21/16/audi-1283853_1280.jpg',
        'description': 'High-performance sports car built for speed and handling.',
    },
    {
        'id': 4,
        'title': 'Classic Muscle',
        'image': 'https://cdn.pixabay.com/photo/2013/07/12/15/55/mustang-150318_1280.png',
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
