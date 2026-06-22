from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages  
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Form aur Formset Imports
from .forms import SignUpForm, PropertyForm, PropertyImageFormSet  
# Model Data Engine Imports
from .models import Property, Inquiry, Wishlist, PropertyImage  

# ==========================================================================
# 🏠 1. HOMEPAGE VIEW (With Search & Filter Logic)
# ==========================================================================
def home(request):
    queryset = Property.objects.all().order_by('-created_at')[:6]
    
    location_query = request.GET.get('location')
    type_query = request.GET.get('property_type')
    price_query = request.GET.get('max_price')

    # Agar koi bhi filter active hai, toh slicing hata kar results fetch karenge
    if (location_query and location_query.strip()) or type_query or price_query:
        queryset = Property.objects.all().order_by('-created_at')
        
        if location_query and location_query.strip():
            # Yeh exact hotspot ya matching substring dono ko nikal lega
            queryset = queryset.filter(location__icontains=location_query.strip())
        if type_query and type_query != '':
            queryset = queryset.filter(property_type=type_query)
        if price_query and price_query != '':
            queryset = queryset.filter(price__lte=int(price_query))
        
    user_wishlist_ids = []
    if request.user.is_authenticated:
        user_wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('property_id', flat=True)
        
    return render(request, 'properties/home.html', {
        'properties': queryset,
        'user_wishlist_ids': user_wishlist_ids
    })


# ==========================================================================
# 🌐 2. ALL PROPERTIES VIEW (Catalog Display Grid)
# ==========================================================================
def all_properties_view(request):
    queryset = Property.objects.all().order_by('-created_at')
    
    user_wishlist_ids = []
    if request.user.is_authenticated:
        user_wishlist_ids = Wishlist.objects.filter(user=request.user).values_list('property_id', flat=True)
        
    return render(request, 'properties/all_properties.html', {
        'properties': queryset,
        'user_wishlist_ids': user_wishlist_ids
    })


# ==========================================================================
# 🔍 3. PROPERTY DETAIL VIEW (With Carousel Display Support)
# ==========================================================================
def property_detail(request, pk):
    property_single = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_text = request.POST.get('message')
        
        inquiry = Inquiry(
            property=property_single,
            name=name,
            email=email,
            phone=phone,
            message=message_text
        )
        
        if request.user.is_authenticated:
            inquiry.user = request.user
            
        inquiry.save()
        
        messages.success(request, 'Your message has been sent successfully! The agent will contact you soon.')
        return redirect('property_detail', pk=property_single.id)

    return render(request, 'properties/property_detail.html', {'property': property_single})


# ==========================================================================
# 🔐 4. AUTHENTICATION MODULE CONTROLLERS (Signup / Login / Logout)
# ==========================================================================
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Auto-login after registration context setup
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'properties/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'properties/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# ==========================================================================
# 🏗️ 5. PROPERTY MANAGEMENT WORKSPACE (Add / Delete)
# ==========================================================================
@login_required(login_url='login')
def add_property_view(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        formset = PropertyImageFormSet(request.POST, request.FILES)
        
        if form.is_valid() and formset.is_valid():
            property_instance = form.save(commit=False)
            property_instance.user = request.user  # Assigning property to current user log
            property_instance.save()
            
            # Formset parameters mapped to primary key entity context 
            formset.instance = property_instance
            formset.save()
            
            messages.success(request, 'Your property and gallery images have been listed successfully!')
            return redirect('dashboard')
    else:
        form = PropertyForm()
        formset = PropertyImageFormSet()
        
    return render(request, 'properties/add_property.html', {
        'form': form,
        'formset': formset
    })


@login_required(login_url='login')
def delete_property_view(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id, user=request.user)
    if request.method == 'POST':
        property_obj.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('dashboard')
    return redirect('dashboard')


# ==========================================================================
# 📊 6. CRM DASHBOARD & WISHLIST MODULE ENGINE
# ==========================================================================
@login_required(login_url='login')
def toggle_wishlist(request, property_id):
    property_obj = get_object_or_404(Property, id=property_id)
    wishlist_item = Wishlist.objects.filter(user=request.user, property=property_obj)
    
    if wishlist_item.exists():
        wishlist_item.delete()
        messages.info(request, 'Property removed from your wishlist.')
    else:
        Wishlist.objects.create(user=request.user, property=property_obj)
        messages.success(request, 'Property added to your wishlist!')
        
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def dashboard_view(request):
    # User listings dataset setup
    my_properties = Property.objects.filter(user=request.user).order_by('-created_at')
    # Incoming Leads pipeline tracking node
    received_leads = Inquiry.objects.filter(property__user=request.user).order_by('-created_at')
    # User saved/favorites dataset cache
    my_wishlist = Wishlist.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'my_properties': my_properties,
        'received_leads': received_leads,
        'my_wishlist': my_wishlist,
    }
    return render(request, 'properties/dashboard.html', context)
# ==========================================================================
# 📄 STATIC PAGES CONTROLLERS (About, Services, Contact)
# ==========================================================================

def about_view(request):
    return render(request, 'properties/about.html')

def services_view(request):
    return render(request, 'properties/services.html')

def contact_view(request):
    # Agar contact page par alag se feedback/message handle karna ho toh baad me post validation jod sakte hain
    if request.method == 'POST':
        messages.success(request, 'Thank you for contacting DigiEstate! Our team will get back to you within 24 hours.')
        return redirect('contact')
    return render(request, 'properties/contact.html')
