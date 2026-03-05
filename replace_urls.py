import os

replacements = {
    "http://192.168.0.106:8000": "http://192.168.0.106:8000",
    "http://192.168.0.106:8001": "http://192.168.0.106:8001",
    "http://192.168.0.106:8002": "http://192.168.0.106:8002",
    "http://192.168.0.106:8003": "http://192.168.0.106:8003",
    "http://192.168.0.106:8000": "http://192.168.0.106:8000"
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
        if file.endswith('.html') or file.endswith('.py') or file.endswith('.bat') or file.endswith('.js') or file.endswith('.md'):
            replace_in_file(os.path.join(root, file))
