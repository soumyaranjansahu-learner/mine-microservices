import subprocess
import re
import time
import json
import os

services = {
    "gateway": 8000,
    "kitchen": 8001,
    "shop": 8002,
    "music": 8003
}

urls = {}
processes = []

for name, port in services.items():
    print(f"Starting tunnel for {name} on port {port}...")
    # cloudflared logs to stderr
    cmd = ["cloudflared.exe", "tunnel", "--url", f"http://127.0.0.1:{port}"]
    
    # We use CREATE_NEW_PROCESS_GROUP on Windows to keep it running
    # but for simplicity, Popen with stdout=PIPE, stderr=PIPE
    p = subprocess.Popen(
        cmd, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE, 
        text=True,
        bufsize=1, # Line buffered
        universal_newlines=True
    )
    processes.append(p)
    
    # Read stderr line by line until we find the URL
    url = None
    # Wait max 15 seconds per tunnel
    start_time = time.time()
    while time.time() - start_time < 15:
        line = p.stderr.readline()
        if line:
            # print(f"[{name}] {line.strip()}")
            match = re.search(r'(https://[a-zA-Z0-9-]+\.trycloudflare\.com)', line)
            if match:
                url = match.group(1)
                break
        else:
            time.sleep(0.1)
            
    if url:
        print(f"[{name}] Success! URL: {url}")
        urls[name] = url
    else:
        print(f"[{name}] Failed to get URL!")

print("\n--- TUNNELS ESTABLISHED ---")
print(json.dumps(urls, indent=4))

# Write to file
with open("tunnels.json", "w") as f:
    json.dump(urls, f, indent=4)

print("\nTunnels are running in the background. Do not close this script.")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    for p in processes:
        p.terminate()
