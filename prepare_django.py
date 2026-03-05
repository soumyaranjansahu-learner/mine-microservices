import os
import re

context_processor_code = """import os
def service_urls(request):
    return {
        'GATEWAY_URL': os.environ.get('GATEWAY_URL', 'http://127.0.0.1:8000'),
        'KITCHEN_URL': os.environ.get('KITCHEN_URL', 'http://127.0.0.1:8001'),
        'SHOP_URL': os.environ.get('SHOP_URL', 'http://127.0.0.1:8002'),
        'MUSIC_URL': os.environ.get('MUSIC_URL', 'http://127.0.0.1:8003'),
    }
"""

projects = ['mine_main', 'mine_kitchen', 'mine_shop', 'mine_music']
base_dir = r"c:\Users\dm2so\Desktop\Mine-Project"

for proj in projects:
    proj_dir = os.path.join(base_dir, proj, proj)
    
    # Write context_processors.py
    with open(os.path.join(proj_dir, 'context_processors.py'), 'w') as f:
        f.write(context_processor_code)
        
    # Update settings.py
    settings_path = os.path.join(proj_dir, 'settings.py')
    with open(settings_path, 'r') as f:
        content = f.read()

    # 1. ALLOWED_HOSTS
    if "ALLOWED_HOSTS = ['*']" not in content:
        content = re.sub(r"ALLOWED_HOSTS = \[.*?\]", "ALLOWED_HOSTS = ['*']", content)
        
    # 2. Whitenoise Middleware
    if "whitenoise.middleware.WhiteNoiseMiddleware" not in content:
        content = content.replace(
            "'django.middleware.security.SecurityMiddleware',",
            "'django.middleware.security.SecurityMiddleware',\n    'whitenoise.middleware.WhiteNoiseMiddleware',"
        )
        
    # 3. Context Processor
    cp_string = f"'{proj}.context_processors.service_urls',"
    if cp_string not in content:
        content = content.replace(
            "'django.template.context_processors.request',",
            f"'django.template.context_processors.request',\n                {cp_string}"
        )
        
    # 4. STATIC_ROOT
    if "STATIC_ROOT" not in content:
        content += "\nimport os\nSTATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')\nSTATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'\n"
        
    with open(settings_path, 'w') as f:
        f.write(content)
        
    print(f"Updated {settings_path}")
