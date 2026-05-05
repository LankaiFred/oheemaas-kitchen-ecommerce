"""
Models for the restaurant app
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class MenuCategory(models.Model):
    """Menu category model"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = 'Menu Categories'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Menu item model"""
    category = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='menu_items/', blank=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    preparation_time = models.IntegerField(help_text='Preparation time in minutes', default=15)
    spicy_level = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        help_text='Spice level 0-5'
    )
    calories = models.IntegerField(blank=True, null=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    """Shopping cart model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopping_cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_total(self):
        """Calculate cart total"""
        return sum(item.get_subtotal() for item in self.items.all())


class CartItem(models.Model):
    """Shopping cart item model"""
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    special_instructions = models.TextField(blank=True)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_subtotal(self):
        """Calculate item subtotal"""
        return self.menu_item.price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"


class Order(models.Model):
    """Order model"""
    DELIVERY_CHOICES = (
        ('delivery', 'Delivery'),
        ('pickup', 'Pickup'),
    )
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=50, unique=True)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    delivery_address = models.TextField(blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    estimated_delivery_time = models.DateTimeField(blank=True, null=True)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.order_number}"


class OrderItem(models.Model):
    """Order item model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    special_instructions = models.TextField(blank=True)

    def get_subtotal(self):
        """Calculate item subtotal"""
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"


class Reservation(models.Model):
    """Reservation model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    guest_count = models.IntegerField(validators=[MinValueValidator(1)])
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-reservation_date', '-reservation_time']

    def __str__(self):
        return f"Reservation for {self.user.username} on {self.reservation_date}"


class Payment(models.Model):
    """Payment model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, unique=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.status}"


class RestaurantInfo(models.Model):
    """Restaurant information model"""
    name = models.CharField(max_length=255)
    description = models.TextField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='restaurant/', blank=True)
    banner_image = models.ImageField(upload_to='restaurant/', blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=5)
    minimum_order = models.DecimalField(max_digits=10, decimal_places=2, default=10)
    max_delivery_distance = models.IntegerField(default=15, help_text='Maximum delivery distance in km')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Restaurant Info'

    def __str__(self):
        return self.name


class OpeningHours(models.Model):
    """Opening hours model"""
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    day_of_week = models.IntegerField(choices=DAY_CHOICES)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Opening Hours'
        unique_together = ('day_of_week',)

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.opening_time} - {self.closing_time}"


class ContactMessage(models.Model):
    """Contact message model"""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"
