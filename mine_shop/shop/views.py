from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from .models import Category, Product, CartItem, Order, OrderItem
from .serializers import CategorySerializer, ProductSerializer, CartItemSerializer, OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if category:
            queryset = queryset.filter(category_id=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        quantity = int(self.request.data.get('quantity', 1))
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
                if quantity > product.stock:
                    raise ValidationError({'error': f'Not enough stock available for {product.name}'})
            except Product.DoesNotExist:
                pass
        serializer.save(user_id=self.request.user.id)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['Pending', 'Paid']:
            return Response({'error': 'Order cannot be cancelled in its current state.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'Cancelled'
        order.save()
        
        # Restore stock
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
            
        return Response({'message': 'Order cancelled successfully.'})

    @action(detail=True, methods=['post'])
    def return_order(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['Delivered', 'Paid']:
            return Response({'error': 'Order cannot be returned in its current state.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'Returned'
        order.save()
        
        # Restore stock
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
            
        return Response({'message': 'Order returned successfully.'})

    @action(detail=True, methods=['post'])
    def exchange(self, request, pk=None):
        order = self.get_object()
        if order.status not in ['Delivered', 'Paid']:
            return Response({'error': 'Order cannot be exchanged in its current state.'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.status = 'Exchanged'
        order.save()
        
        return Response({'message': 'Order marked for exchange.'})

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        cart_items = CartItem.objects.filter(user_id=user_id)
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        shipping_address = request.data.get('shipping_address', '').strip()
        if not shipping_address:
            return Response({'error': 'Shipping address is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check stock before accepting checkout
        for item in cart_items:
            if item.quantity > item.product.stock:
                return Response({'error': f'Not enough stock for {item.product.name}. Available: {item.product.stock}'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.product.price * item.quantity for item in cart_items)
        
        payment_method = request.data.get('payment_method', 'Card')
        contact_number = request.data.get('contact_number', '')
        
        # Fake payment processing simulation happens here
        
        # Create Order
        order = Order.objects.create(
            user_id=user_id, 
            total_amount=total_amount, 
            status='Paid', 
            payment_method=payment_method,
            shipping_address=shipping_address,
            contact_number=contact_number
        )
        
        # Decrement stock and save items
        for item in cart_items:
            item.product.stock -= item.quantity
            item.product.save()
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        
        # Clear Cart
        cart_items.delete()
        return Response({'message': 'Checkout successful', 'order_id': order.id}, status=status.HTTP_200_OK)

# --- UI Views ---
from django.shortcuts import render

def shop_home(request):
    return render(request, 'shop.html')

def shop_cart(request):
    return render(request, 'cart.html')

def shop_orders(request):
    return render(request, 'orders.html')

def shop_checkout_success(request):
    return render(request, 'checkout_success.html')

def shop_payment(request):
    return render(request, 'payment.html')

def shop_product_detail(request, product_id):
    return render(request, 'product_detail.html', {'product_id': product_id})
