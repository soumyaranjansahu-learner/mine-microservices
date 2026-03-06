from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from .models import FoodItem, CartItem, Order
from .serializers import FoodItemSerializer, CartItemSerializer, OrderSerializer

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer
    
    def get_queryset(self):
        queryset = FoodItem.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        min_price = self.request.query_params.get('min_price', None)
        max_price = self.request.query_params.get('max_price', None)
        
        if category and category != 'All':
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(name__icontains=search)
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
            
        return queryset

    @action(detail=False, methods=['get'])
    def categories(self, request):
        categories = FoodItem.objects.values_list('category', flat=True).distinct()
        return Response([cat for cat in categories if cat])
        
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

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.user.id
        cart_items = CartItem.objects.filter(user_id=user_id)
        
        if not cart_items.exists():
            return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        shipping_address = request.data.get('shipping_address', '').strip()
        if not shipping_address:
            return Response({'error': 'Shipping address is required'}, status=status.HTTP_400_BAD_REQUEST)

        total_amount = sum(item.food_item.price * item.quantity for item in cart_items)
        
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
        
        # Clear Cart
        cart_items.delete()
        return Response({'message': 'Checkout successful', 'order_id': order.id}, status=status.HTTP_200_OK)

# --- UI Views ---
from django.shortcuts import render

def kitchen_home(request):
    return render(request, 'kitchen.html')

def kitchen_cart(request):
    return render(request, 'cart.html')

def kitchen_orders(request):
    return render(request, 'orders.html')

def kitchen_checkout_success(request):
    return render(request, 'checkout_success.html')

def kitchen_payment(request):
    return render(request, 'payment.html')

def kitchen_food_detail(request, food_id):
    return render(request, 'food_detail.html', {'food_id': food_id})
