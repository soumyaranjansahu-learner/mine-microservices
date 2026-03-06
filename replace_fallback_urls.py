import os

REPLACEMENTS = {
    'https://mine-gateway.onrender.com': 'https://mine-gateway.onrender.com',
    'https://mine-kitchen.onrender.com': 'https://mine-kitchen.onrender.com',
    'https://mine-shop.onrender.com': 'https://mine-shop.onrender.com',
    'https://mine-music.onrender.com': 'https://mine-music.onrender.com',
}

def replace_in_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for old, new in REPLACEMENTS.items():
        if old in content:
            content = content.replace(old, new)
            modified = True
            
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filepath}")

if __name__ == '__main__':
    project_root = r'c:\Users\dm2so\Desktop\Mine-Project'
    for root, dirs, files in os.walk(project_root):
        if 'venv' in root or '.git' in root:
            continue
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                replace_in_file(filepath)
    print("Done replacing fallback URLs.")
