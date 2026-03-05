from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    home_view, login_view, logout_view, register_view, gateway_view, global_search_view
)

urlpatterns = [
    # Template URLs
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    
    # Auth URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Global Search API
    path('api/search/', global_search_view, name='global_search'),
    
    # Gateway URL mapping
    path('api/<str:service>/<path:path>', gateway_view, name='gateway'),
]
