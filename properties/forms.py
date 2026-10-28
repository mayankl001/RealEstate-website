from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import Property, PropertyImage, Inquiry


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class PropertyForm(forms.ModelForm):
    """
    Form for creating and editing property listings.
    """
    class Meta:
        model = Property
        fields = [
            'title',
            'location',
            'property_type',
            'price',
            'bedrooms',
            'bathrooms',
            'area_sqft',
            'main_image',
            'description',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 3 BHK Luxury Apartment'
            }),
            'location': forms.Select(attrs={
                'class': 'form-select'
            }),
            'property_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 4500000'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 3'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2'
            }),
            'area_sqft': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 1500'
            }),
            'main_image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe features, nearby landmarks, society facilities, etc.'
            }),
        }


# FormSet for uploading multiple additional gallery images
PropertyImageFormSet = inlineformset_factory(
    parent_model=Property,
    model=PropertyImage,
    fields=['image', 'alt_text'],
    extra=4,  # Shows 4 extra image upload slots
    max_num=6,  # Maximum 6 gallery images
    can_delete=True,
    widgets={
        'image': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
        'alt_text': forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'e.g. Living Room, Balcony'
        }),
    }
)


class InquiryForm(forms.ModelForm):
    """
    Form for direct customer property inquiries.
    """
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Your inquiry message...'}),
        }