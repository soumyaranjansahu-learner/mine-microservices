from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    features = models.JSONField(blank=True, null=True, default=dict)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected_features = models.JSONField(blank=True, null=True, default=dict)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} for User {self.user_id}"

class Order(models.Model):
    user_id = models.IntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    payment_method = models.CharField(max_length=50, default='Card')
    shipping_address = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    action_reason = models.TextField(blank=True, null=True)
    refund_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by User {self.user_id} via {self.payment_method}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selected_features = models.JSONField(blank=True, null=True, default=dict)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.id}"
