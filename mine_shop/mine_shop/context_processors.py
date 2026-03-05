import os
def service_urls(request):
    return {
        'GATEWAY_URL': os.environ.get('GATEWAY_URL', 'http://127.0.0.1:8000'),
        'KITCHEN_URL': os.environ.get('KITCHEN_URL', 'http://127.0.0.1:8001'),
        'SHOP_URL': os.environ.get('SHOP_URL', 'http://127.0.0.1:8002'),
        'MUSIC_URL': os.environ.get('MUSIC_URL', 'http://127.0.0.1:8003'),
    }
