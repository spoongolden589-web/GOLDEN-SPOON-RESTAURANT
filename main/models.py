from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from decimal import Decimal


class UserProfile(models.Model):
    """Extended user profile for additional information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"


class MenuItem(models.Model):
    """Menu items with details and allergen information"""
    CATEGORY_CHOICES = [
        ('starter', 'Starters'),
        ('main', 'Main Courses'),
        ('dessert', 'Desserts'),
        ('drink', 'Drinks'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    ingredients = models.TextField(help_text="List of ingredients")
    allergens = models.TextField(blank=True, help_text="Allergen information")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} - £{self.price}"


class Order(models.Model):
    """Customer orders with delivery/collection options"""
    ORDER_TYPE_CHOICES = [
        ('delivery', 'Delivery'),
        ('collection', 'Collection'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Collection'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    order_number = models.CharField(max_length=32, unique=True, editable=False)
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Guest user information
    guest_name = models.CharField(max_length=200, blank=True)
    guest_email = models.EmailField(blank=True)
    guest_phone = models.CharField(max_length=20, blank=True)
    
    # Delivery details
    delivery_address = models.TextField(blank=True)
    
    # Collection details
    collection_time = models.DateTimeField(blank=True, null=True)
    
    # Pricing
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Payment
    payment_method = models.CharField(max_length=50, default='card')
    payment_token = models.CharField(max_length=200, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        if self.user:
            return f"Order {self.order_number} - {self.user.username}"
        else:
            return f"Order {self.order_number} - Guest ({self.guest_name})"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            import uuid
            self.order_number = uuid.uuid4().hex[:16].upper()
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Individual items within an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=6, decimal_places=2)  # Price at time of order
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} in Order {self.order.order_number}"
    
    def get_total(self):
        return self.quantity * self.price


class Reservation(models.Model):
    """Table reservation system"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', null=True, blank=True)
    reservation_number = models.CharField(max_length=32, unique=True, editable=False)
    date = models.DateField()
    time = models.TimeField()
    guests = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Guest user information
    guest_name = models.CharField(max_length=200, blank=True)
    guest_email = models.EmailField(blank=True)
    guest_phone = models.CharField(max_length=20, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
        unique_together = ['date', 'time']  # Prevent double bookings
    
    def __str__(self):
        if self.user:
            return f"Reservation {self.reservation_number} - {self.user.username} on {self.date}"
        else:
            return f"Reservation {self.reservation_number} - Guest ({self.guest_name}) on {self.date}"
    
    def save(self, *args, **kwargs):
        if not self.reservation_number:
            import uuid
            self.reservation_number = uuid.uuid4().hex[:16].upper()
        super().save(*args, **kwargs)
