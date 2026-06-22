from django.contrib import admin
from .models import Property, Inquiry, Wishlist, PropertyImage

# Inline image layout setup
class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3  # By default admin ko 3 khali slots dikhenge extra images ke liye

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price', 'property_type', 'created_at')
    search_fields = ('title', 'location')
    list_filter = ('property_type', 'created_at')
    inlines = [PropertyImageInline]  # Isse multi-image upload active ho jayega

# Baaki models register karein
admin.site.register(Inquiry)
admin.site.register(Wishlist)
admin.site.register(PropertyImage)