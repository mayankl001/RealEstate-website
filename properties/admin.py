from django.contrib import admin
from .models import Property, PropertyImage, Inquiry, Wishlist


class PropertyImageInline(admin.TabularInline):
    """
    Allows editing gallery images directly inside the Property admin page.
    """
    model = PropertyImage
    extra = 3
    fields = ('image', 'alt_text')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'property_type', 'price', 'location', 'bedrooms', 'bathrooms', 'created_at')
    list_filter = ('property_type', 'location', 'created_at')
    search_fields = ('title', 'location', 'description', 'user__username')
    inlines = [PropertyImageInline]
    ordering = ('-created_at',)


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'alt_text', 'image')
    search_fields = ('property__title', 'alt_text')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'property', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone', 'property__title', 'message')
    readonly_fields = ('created_at',)


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'property', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'property__title')