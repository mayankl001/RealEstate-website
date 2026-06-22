from django.db import models
from django.contrib.auth.models import User

class Property(models.Model):
    PROPERTY_TYPES = [
        ('SALE', 'For Sale'),
        ('RENT', 'For Rent'),
    ]

    # 📍 Ranchi ke Major Hotspots Choices Array
    RANCHI_HOTSPOTS = [
        ('Lalpur', 'Lalpur'),
        ('Kanke Road', 'Kanke Road'),
        ('Doranda', 'Doranda'),
        ('Bariatu', 'Bariatu'),
        ('Kokar', 'Kokar'),
        ('Namkum', 'Namkum'),
        ('Argora', 'Argora / Harmu'),
        ('Ratu Road', 'Ratu Road'),
    ]

    # ✨ DASHBOARD LINK: Yeh batayega ki property kisne list ki hai (Broker/User)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # 🔄 Location field ko CharField se choices me link kar diya
    location = models.CharField(max_length=100, choices=RANCHI_HOTSPOTS, default='Lalpur')
    
    price = models.IntegerField()
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area_sqft = models.IntegerField()
    property_type = models.CharField(max_length=10, choices=PROPERTY_TYPES, default='SALE')
    main_image = models.ImageField(upload_to='properties/') 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Properties"

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    # Optional connection for logged in users, drops to NULL if user deletes profile
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # Linked property for incoming lead notifications
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inquiries"

    def __str__(self):
        return f"Inquiry by {self.name} for {self.property.title}"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Ek user ek property ko ek hi baar wishlist me daal sakta hai (Anti-Duplication)
        unique_together = ('user', 'property')
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"{self.user.username} saved {self.property.title}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/gallery/')
    alt_text = models.CharField(max_length=100, blank=True, help_text="e.g. Living Room, Kitchen")

    class Meta:
        verbose_name = "Property Image"
        verbose_name_plural = "Property Images"

    def __str__(self):
        return f"Image for {self.property.title}"
    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_gallery/')
    alt_text = models.CharField(max_length=200, blank=True, null=True, help_text="Optional: Image description")

    def __str__(self):
        return f"Image for {self.property.title}"    