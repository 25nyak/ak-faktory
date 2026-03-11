import requests
import time
import subprocess
import random

# --- CONFIGURATION ---
API_KEY = eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDQ3MjU5NjIsImlhdCI6MTc3MzE4OTk2MiwicmF5IjoiZDc5ZTk1MDI2M2M2YmRlNGU5NmI2ZjBjNWYyNDA5NzIiLCJzdWIiOjM4NjM3ODh9.KxKXWR01OfQBRrIHFzQU5OCxeB8XkiFid1gzZ_nNE_byiJrbUAAnr6rWV47AmpuBbGhYpke-kOsSsJit4716KeRtAd7U_uNtS-z9EfSjUEx2xh0hZ9txF5gkKqO2Tb91jghQhMUaZg1yZM0w6wid68Kdpdp2gF3zxOow_AvY3ONNm47S4YKtL4kHFQgx-z_2qmUXJDV5YcFCPJrcll7RKP9fRUT5toSKTBY4wcIciuKOQx8qNRQKviTcYHpE7Cikj2SsS8Dj1UbXEOEZOpYaiUl56tn9So_rZYB7jm-xUKh-0WTH2UB1kg2_c9wCTrF7v45Y76Kcgu2F0PNo7I_XxQ
ADB_PATH = "adb"
# Default LDPlayer ports (5554, 5556, etc.)
PORTS = ["5554", "5556", "5558"] 

def adb_type(device_id, text):
    subprocess.run([ADB_PATH, "-s", device_id, "shell", "input", "text", text])

def get_tg_number():
    """Requests a Telegram number from the API."""
    url = f"https://api.sms-activate.org/storio/v2/get_number?api_key={API_KEY}&service=tg&country=0" # 0 is generic/cheap
    res = requests.get(url).json()
    if res.get('status') == 'SUCCESS':
        return res['id'], res['number']
    return None, None

def get_sms_code(activation_id):
    """Polls the API for the 5-digit Telegram code."""
    print("[*] Waiting for SMS (this can take 2-5 minutes)...")
    for _ in range(30):
        url = f"https://api.sms-activate.org/storio/v2/get_status?api_key={API_KEY}&id={activation_id}"
        res = requests.get(url).json()
        if res.get('status') == 'STATUS_OK':
            return res['code']
        time.sleep(10)
    return None

def run_factory():
    for port in PORTS:
        device_id = f"127.0.0.1:{port}"
        print(f"\n[#] UNIT {device_id} ACTIVE")
        
        # 1. Get Number
        act_id, phone = get_tg_number()
        if not phone:
            print("[-] Out of stock or API error.")
            continue
            
        print(f"[+] Assigned Number: {phone}")
        
        # 2. Type into LDPlayer (Assumes Telegram is open on the 'Start' screen)
        # Note: You might need to manually click the 'Start Messaging' button first
        adb_type(device_id, phone)
        subprocess.run([ADB_PATH, "-s", device_id, "shell", "input", "keyevent", "66"]) # Enter
        
        # 3. Wait for Code
        code = get_sms_code(act_id)
        if code:
            print(f"[!] Code Received: {code}")
            adb_type(device_id, code)
            print(f"[SUCCESS] Unit {device_id} is registered.")
            # Add Bio/Profile Setup here
        else:
            print("[-] Timeout: No SMS received. Cancelling activation...")
            requests.get(f"https://api.sms-activate.org/storio/v2/set_status?api_key={API_KEY}&id={act_id}&status=8")

if __name__ == "__main__":
    run_factory()
