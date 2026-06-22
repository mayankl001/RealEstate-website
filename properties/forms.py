from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .models import Property, PropertyImage

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        # Hum user se ye saari fields frontend par bharwayenge
        fields = ['title', 'description', 'location', 'price', 'bedrooms', 'bathrooms', 'area_sqft', 'property_type', 'main_image']
        
        # Form ko Bootstrap styling dene ke liye widgets setup
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Modern 3 BHK Flat'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your property...'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Lalpur, Ranchi'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price in INR'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'area_sqft': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1200'}),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'main_image': forms.FileInput(attrs={'class': 'form-control'}),
        }   



PropertyImageFormSet = inlineformset_factory(
    Property,          # Parent Model
    PropertyImage,     # Child Model (Gallery Image)
    fields=['image', 'alt_text'],
    extra=4,           # Front-end par user ko ek saath 4 extra empty image slots dikhenge
    max_num=10,        # Ek property me max 10 images allow hongi
    can_delete=True,   # Edit karte waqt user purani images delete bhi kar payega
    widgets={
        'image': forms.FileInput(attrs={
            'class': 'form-control', 
            'accept': 'image/*'  # Browser me sirf images select karne ka filter trigger hoga
        }),
        'alt_text': forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'e.g., Master Bedroom, Spacious Kitchen'
        }),
    }
)