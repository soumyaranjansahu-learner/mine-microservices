import os
def service_urls(request):
    return {
        'GATEWAY_URL': os.environ.get('GATEWAY_URL', 'https://mine-gateway.onrender.com'),
        'KITCHEN_URL': os.environ.get('KITCHEN_URL', 'https://mine-kitchen.onrender.com'),
        'SHOP_URL': os.environ.get('SHOP_URL', 'https://mine-shop.onrender.com'),
        'MUSIC_URL': os.environ.get('MUSIC_URL', 'https://mine-music.onrender.com'),
    }
