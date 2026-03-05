import requests
from django.shortcuts import render, redirect
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Template Views
def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        
        # Generate JWT token
        response = requests.post(
            f'http://127.0.0.1:8000/api/token/',
            data={'username': username, 'password': password}
        )
        if response.status_code == 200:
            request.session['jwt_token'] = response.json().get('access')
            return redirect('home')
        return redirect('home')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        # Simulated authentication for simplicity
        # In a real app we would use a proper form and DRF JWT token obtain
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # Generate JWT token by calling our own API
            # For simplicity we simulate setting a dummy token in session
            # In production we'd call the TokenObtainPairView logic
            
            response = requests.post(
                f'http://127.0.0.1:8000/api/token/',
                data={'username': username, 'password': password}
            )
            if response.status_code == 200:
                request.session['jwt_token'] = response.json().get('access')
                return redirect('home')
            else:
                return render(request, 'login.html', {'error': 'Failed to obtain token'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    if 'jwt_token' in request.session:
        del request.session['jwt_token']
    return redirect('login')

# Global Search View
@api_view(['GET'])
@permission_classes([AllowAny])
def global_search_view(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({'results': []})
        
    # Forward the JWT token if it exists in the session
    headers = {}
    token = request.session.get('jwt_token')
    if token:
        headers['Authorization'] = f'Bearer {token}'
        
    results = []
    
    # Try fetching from Shop
    try:
        res = requests.get(f'http://127.0.0.1:8002/api/products/?search={query}', headers=headers, timeout=2)
        if res.status_code == 200:
            for item in res.json():
                results.append({
                    'type': 'shop',
                    'id': item['id'],
                    'name': item['name'],
                    'description': item['description'][:100] + '...' if len(item['description']) > 100 else item['description'],
                    'price': item['price'],
                    'image_url': item.get('image_url', ''),
                })
    except Exception:
        pass
        
    # Try fetching from Kitchen
    try:
        res = requests.get(f'http://127.0.0.1:8001/api/foods/?search={query}', headers=headers, timeout=2)
        if res.status_code == 200:
            for item in res.json():
                results.append({
                    'type': 'kitchen',
                    'id': item['id'],
                    'name': item['name'],
                    'description': item['description'][:100] + '...' if len(item['description']) > 100 else item['description'],
                    'price': item['price'],
                    'image_url': item.get('image_url', ''),
                    'category': item.get('category', 'General')
                })
    except Exception:
        pass
        
    # Try fetching from Music
    try:
        res = requests.get(f'http://127.0.0.1:8003/api/songs/?search={query}', headers=headers, timeout=2)
        if res.status_code == 200:
            for item in res.json():
                results.append({
                    'type': 'music',
                    'id': item['id'],
                    'name': item['title'],
                    'description': f"Artist: {item['artist']}",
                    'image_url': item.get('cover_image_url', ''),
                    'genre': item.get('genre', 'Unknown')
                })
    except Exception:
        pass
        
    return Response({'results': results})

# Gateway Routing View
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([AllowAny])
def gateway_view(request, service, path):
    # Service Map
    services = {
        'kitchen': 'http://127.0.0.1:8001/',
        'shop': 'http://127.0.0.1:8002/',
        'music': 'http://127.0.0.1:8003/',
    }
    
    if service not in services:
        return JsonResponse({'error': 'Service not found'}, status=404)
        
    target_url = f"{services[service]}{path}"
    
    # Forward the JWT token if it exists in the session
    headers = {}
    token = request.session.get('jwt_token')
    if token:
        headers['Authorization'] = f'Bearer {token}'
        
    # Content-type
    if request.content_type:
        headers['Content-Type'] = request.content_type

    try:
        if request.method == 'GET':
            response = requests.get(target_url, headers=headers, params=request.GET)
        elif request.method == 'POST':
            response = requests.post(target_url, headers=headers, json=request.data if request.content_type == 'application/json' else request.POST)
        elif request.method == 'PUT':
            response = requests.put(target_url, headers=headers, json=request.data)
        elif request.method == 'PATCH':
            response = requests.patch(target_url, headers=headers, json=request.data)
        elif request.method == 'DELETE':
            response = requests.delete(target_url, headers=headers)
        
        # Return response from microservice
        try:
             return Response(response.json(), status=response.status_code)
        except ValueError:
             return HttpResponse(response.content, status=response.status_code, content_type=response.headers.get('Content-Type'))
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f'Failed to connect to {service} service: {str(e)}'}, status=503)
