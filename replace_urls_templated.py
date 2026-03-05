import os

replacements = {
    "http://192.168.0.106:8000": "{{ GATEWAY_URL }}",
    "http://192.168.0.106:8001": "{{ KITCHEN_URL }}",
    "http://192.168.0.106:8002": "{{ SHOP_URL }}",
    "http://192.168.0.106:8003": "{{ MUSIC_URL }}",
}

def replace_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for old, new in replacements.items():
            new_content = new_content.replace(old, new)
            
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {filepath}")
    except UnicodeDecodeError:
        pass

for root, dirs, files in os.walk(r'c:\Users\dm2so\Desktop\Mine-Project'):
    if 'venv' in root or '.git' in root:
        continue
    for file in files:
        if file.endswith('.html'):
            replace_in_file(os.path.join(root, file))
