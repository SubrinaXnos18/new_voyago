from django.urls import path
from . import views
from .views import custom_register
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('bookings/', views.bookings, name='bookings'),
    path('payment/<int:package_id>/', views.payment, name='payment'),
    path('register/', custom_register, name='register'),
    path('my-diary/', views.my_diary, name='my_diary'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-panel/add/', views.add_package, name='add_package'),
    path('admin-panel/edit/<int:package_id>/', views.edit_package, name='edit_package'),
    path('admin-panel/delete/<int:package_id>/', views.delete_package, name='delete_package'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('contact-us/', views.contact_us, name='contact_us'),
]
