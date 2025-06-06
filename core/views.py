from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import Package
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Package, Booking
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import Diary, DiaryImage
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings
from core.forms import PackageForm, ContactForm
from django.contrib import messages


def index(request):
    return render(request, 'core/index.html')


def bookings(request):
    destination = request.GET.get('destination', '')
    checkin = request.GET.get('checkin', '')
    checkout = request.GET.get('checkout', '')
    guests = request.GET.get('guests', '')
    packages = Package.objects.all()
    if destination:
        packages = packages.filter(destination__icontains=destination)
    # Add logic for checkin, checkout, guests if applicable
    return render(request, 'core/bookings.html', {'packages': packages})

@login_required
def payment(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    
    if request.method == "POST":
        Booking.objects.create(user=request.user, package=package)
        return render(request, 'core/thank_you.html', {'package': package})

    return render(request, 'core/payment.html', {'package': package})

def custom_register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(request.POST.get("next", "/"))
    else:
        form = UserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def my_diary(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        text = request.POST.get('text')
        diary = Diary.objects.create(user=request.user, text=text)
        images = request.FILES.getlist('images')
        for image in images:
            DiaryImage.objects.create(diary=diary, image=image)
        return redirect('my_diary')

    entries = Diary.objects.all().order_by('-created_at')  # Fetch all entries for public viewing
    return render(request, 'core/my_diary.html', {'entries': entries})

@staff_member_required
def admin_panel(request):
    packages = Package.objects.all()
    bookings = Booking.objects.select_related('user', 'package').order_by('-booked_on')
    return render(request, 'core/admin_panel.html', {'packages': packages, 'bookings': bookings})

class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

@staff_member_required
def add_package(request):
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package added successfully!')
            return redirect('admin_panel')
        else:
            # Debugging: Log form errors to understand validation issues
            print("Form errors:", form.errors)
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PackageForm()
    return render(request, 'core/package_form.html', {'form': form, 'title': 'Add Package'})

@staff_member_required
def edit_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    if request.method == 'POST':
        form = PackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, 'Package updated successfully!')  # Added success message
            return redirect('admin_panel')
        else:
            print("Form errors:", form.errors)  # Debugging
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = PackageForm(instance=package)
    return render(request, 'core/package_form.html', {'form': form, 'title': 'Edit Package'})

@staff_member_required
def delete_package(request, package_id):
    package = get_object_or_404(Package, id=package_id)
    package.delete()
    return redirect('admin_panel')

# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('bookings')  # Redirect to bookings or any other page you prefer
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

# Register View
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login after registration
    else:
        form = UserCreationForm()

    return render(request, 'core/register.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('index')  # Redirect to homepage after logout


# contact us........>
class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'contact_number', 'comments']

def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('contact_us')  # Redirect to the same page after submission
    else:
        form = ContactForm()
    return render(request, 'core/contact_us.html', {'form': form})




