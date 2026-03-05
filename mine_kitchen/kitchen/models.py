from django.db import models

class FoodItem(models.Model):
    CATEGORY_CHOICES = [
        ('Meals', 'Meals'),
        ('Drinks', 'Drinks'),
        ('Snacks', 'Snacks'),
        ('Desserts', 'Desserts'),
        ('General', 'General'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='General')
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user_id = models.IntegerField() # We store the user ID from the JWT token
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.food_item.name} for User {self.user_id}"

class Order(models.Model):
    user_id = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    payment_method = models.CharField(max_length=50, default='Card')
    shipping_address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by User {self.user_id} via {self.payment_method}"
