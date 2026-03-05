import os
import django
import sys
import tempfile

def test_shop():
    sys.path.append(r"c:\Users\dm2so\Desktop\Mine-Project\mine_shop")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mine_shop.settings')
    django.setup()

    from django.contrib.auth.models import User
    from shop.models import Product, Category, CartItem, Order
    from rest_framework.test import APIClient

    # Setup
    user, _ = User.objects.get_or_create(username='testuser', email='test@test.com')
    user.set_password('testpass')
    user.save()

    cat, _ = Category.objects.get_or_create(name='Electronics')
    prod = Product.objects.create(category=cat, name='Laptop', description='Test', price=1000, stock=5)

    client = APIClient(SERVER_NAME='localhost')
    client.force_authenticate(user=user)

    # Test 1: Add to cart
    print("Testing add to cart...")
    res = client.post('/api/cart/', {'product_id': prod.id, 'quantity': 1})
    assert res.status_code == 201, f"Expected 201, got {res.status_code} {res.data if hasattr(res, 'data') else ''}"

    # Test 2: Add to cart exceeding stock
    res = client.post('/api/cart/', {'product_id': prod.id, 'quantity': 10})
    assert res.status_code == 400, f"Expected 400, got {res.status_code} {res.data if hasattr(res, 'data') else ''}"
    assert 'error' in res.data, "Expected error in response"

    # Test 3: Checkout without address
    print("Testing checkout without address...")
    res = client.post('/api/checkout/', {'payment_method': 'Card', 'shipping_address': ''})
    assert res.status_code == 400, f"Expected 400, got {res.status_code}"
    assert 'Shipping address is required' in str(res.data)

    # Test 4: Checkout with address
    print("Testing checkout with address...")
    res = client.post('/api/checkout/', {'payment_method': 'Card', 'shipping_address': '123 Test St'})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    order_id = res.data['order_id']

    # Check stock decremented
    prod.refresh_from_db()
    assert prod.stock == 4, f"Expected stock 4, got {prod.stock}"

    # Test 5: Cancel order restores stock
    print("Testing cancel order...")
    res = client.post(f'/api/orders/{order_id}/cancel/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    
    prod.refresh_from_db()
    assert prod.stock == 5, f"Expected stock 5, got {prod.stock}"

    print("All shop tests passed!")

if __name__ == '__main__':
    test_shop()
