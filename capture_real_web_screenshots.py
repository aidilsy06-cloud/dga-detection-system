import os
import sys
import time
import subprocess
import requests

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'doc_assets')
os.makedirs(ASSETS_DIR, exist_ok=True)

PAGES = [
    ("real_web_dashboard.png", "http://127.0.0.1:5000/"),
    ("real_web_scanner.png", "http://127.0.0.1:5000/analyst/scanner"),
    ("real_web_batch.png", "http://127.0.0.1:5000/analyst/batch"),
    ("real_web_dns_stream.png", "http://127.0.0.1:5000/analyst/stream"),
    ("real_web_admin_model.png", "http://127.0.0.1:5000/admin/model"),
    ("real_web_admin_threshold.png", "http://127.0.0.1:5000/admin/threshold"),
    ("real_web_admin_firewall.png", "http://127.0.0.1:5000/admin/firewall"),
    ("real_web_admin_dataset.png", "http://127.0.0.1:5000/admin/dataset"),
    ("real_web_admin_api.png", "http://127.0.0.1:5000/admin/api"),
    ("real_web_admin_health.png", "http://127.0.0.1:5000/admin/health"),
    ("real_web_admin_audit.png", "http://127.0.0.1:5000/admin/users"),
]

def main():
    print("[1] Starting Flask server on 127.0.0.1:5000...")
    proc = subprocess.Popen([r"D:\phyton\python.exe", "app.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2.5)

    try:
        r = requests.get("http://127.0.0.1:5000/", timeout=3)
        print("[+] Flask server is active! Status:", r.status_code)
    except Exception as e:
        print("[!] Server failed to start:", e)
        proc.terminate()
        return

    # Simulate some traffic so streams and dashboards are active
    try:
        requests.post("http://127.0.0.1:5000/api/stream/simulate", timeout=2)
        requests.post("http://127.0.0.1:5000/api/stream/simulate", timeout=2)
    except Exception:
        pass

    print("[2] Capturing REAL screenshots via Headless Chrome...")
    for filename, url in PAGES:
        out_file = os.path.join(ASSETS_DIR, filename)
        cmd = [
            CHROME_PATH,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size=1366,768",
            f"--screenshot={out_file}",
            url
        ]
        res = subprocess.run(cmd, capture_output=True)
        if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
            print(f"  [+] Captured {filename} ({os.path.getsize(out_file)} bytes)")
        else:
            print(f"  [!] Failed to capture {filename}: {res.stderr.decode('utf-8', errors='ignore')}")

    proc.terminate()
    print("\n[SUCCESS] All real website screenshots captured successfully!")

if __name__ == "__main__":
    main()
