from django.contrib import admin
from .models import UserProfile, MenuItem, Order, OrderItem, Reservation


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    list_filter = ['created_at']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'created_at']
    list_filter = ['category', 'is_available', 'created_at']
    search_fields = ['name', 'description', 'ingredients']
    list_editable = ['is_available', 'price']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['menu_item', 'quantity', 'price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'user', 'order_type', 'status', 'total', 'created_at']
    list_filter = ['status', 'order_type', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'order_type', 'status')
        }),
        ('Delivery/Collection Details', {
            'fields': ('delivery_address', 'collection_time')
        }),
        ('Pricing', {
            'fields': ('subtotal', 'delivery_fee', 'total')
        }),
        ('Payment', {
            'fields': ('payment_method', 'payment_token')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_number', 'user', 'date', 'time', 'guests', 'status', 'created_at']
    list_filter = ['status', 'date', 'created_at']
    search_fields = ['reservation_number', 'user__username', 'user__email']
    readonly_fields = ['reservation_number', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Reservation Information', {
            'fields': ('reservation_number', 'user', 'date', 'time', 'guests', 'status')
        }),
        ('Additional Details', {
            'fields': ('special_requests',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
