from django.urls import path
from . import views

urlpatterns = [
    # Core Pages
    path('', views.home, name='home'),
    path('properties/', views.all_properties_view, name='all_properties'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    
    # Static Info Pages
    path('about/', views.about_view, name='about'),
    path('services/', views.services_view, name='services'),
    path('contact/', views.contact_view, name='contact'),

    # User Dashboard & Property Actions
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('property/add/', views.add_property_view, name='add_property'),
    path('property/delete/<int:property_id>/', views.delete_property_view, name='delete_property'),
    path('wishlist/toggle/<int:property_id>/', views.toggle_wishlist, name='toggle_wishlist'),

    # Authentication Routes
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]