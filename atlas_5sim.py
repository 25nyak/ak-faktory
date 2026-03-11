import requests
import time
import subprocess
import random

# --- CONFIGURATION ---
API_TOKEN = eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE4MDQ3MjU5NjIsImlhdCI6MTc3MzE4OTk2MiwicmF5IjoiZDc5ZTk1MDI2M2M2YmRlNGU5NmI2ZjBjNWYyNDA5NzIiLCJzdWIiOjM4NjM3ODh9.KxKXWR01OfQBRrIHFzQU5OCxeB8XkiFid1gzZ_nNE_byiJrbUAAnr6rWV47AmpuBbGhYpke-kOsSsJit4716KeRtAd7U_uNtS-z9EfSjUEx2xh0hZ9txF5gkKqO2Tb91jghQhMUaZg1yZM0w6wid68Kdpdp2gF3zxOow_AvY3ONNm47S4YKtL4kHFQgx-z_2qmUXJDV5YcFCPJrcll7RKP9fRUT5toSKTBY4wcIciuKOQx8qNRQKviTcYHpE7Cikj2SsS8Dj1UbXEOEZOpYaiUl56tn9So_rZYB7jm-xUKh-0WTH2UB1kg2_c9wCTrF7v45Y76Kcgu2F0PNo7I_XxQ
ADB_PATH = "adb"
PORTS = ["5554", "5556", "5558"] # Add more as you open more LDPlayers

HEADERS = {
    'Authorization': 'Bearer ' + API_TOKEN,
    'Accept': 'application/json',
}

def get_5sim_number(country='usa', operator='any'):
    """Orders a Telegram number from 5sim."""
    url = f"https://5sim.net/v1/user/buy/activation/{country}/{operator}/telegram"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return res['id'], res['phone']
    except Exception as e:
        print(f"[-] 5sim Error: {e}")
        return None, None

def check_5sim_sms(order_id):
    """Polls 5sim for the 5-digit code."""
    print("[*] Waiting for SMS (Max 5 mins)...")
    for _ in range(30): # 30 attempts, 10 seconds apart
        url = f"https://5sim.net/v1/user/check/{order_id}"
        res = requests.get(url, headers=HEADERS).json()
        
        # 5sim returns a list of SMS objects
        if res.get('sms') and len(res['sms']) > 0:
            return res['sms'][0]['code']
        
        # If the order is cancelled or timed out
        if res.get('status') in ['CANCELED', 'TIMEOUT', 'FINISHED']:
            return None
            
        time.sleep(10)
    return None

def run_factory():
    for port in PORTS:
        device_id = f"127.0.0.1:{port}"
        print(f"\n[#] UNIT {device_id} STARTING...")
        
        # 1. Buy Number
        order_id, phone = get_5sim_number(country='philippines') # Change 'usa' to 'india' or 'russia' for cheaper
        if not phone:
            continue
            
        print(f"[+] Number Acquired: {phone}")
        
        # 2. ADB: Type Number into Telegram
        # This clears the field and types the new number
        subprocess.run([ADB_PATH, "-s", device_id, "shell", "input", "keyevent", "KEYCODE_MOVE_END"])
        for _ in range(15): subprocess.run([ADB_PATH, "-s", device_id, "shell", "input", "keyevent", "67"]) # Backspace
        subprocess.run([ADB_PATH, "-s", device_id, "shell", "input", "text", phone])
        subprocess.run([ADB_PATH, "-s", device_id, "shell", "input", "keyevent", "66"]) # Enter
        
        # 3. Get SMS Code
        code = check_5sim_sms(order_id)
        if code:
            print(f"[!] Code Received: {code}")
            subprocess.run([ADB_PATH, "-s", device_id, "shell", "input", "text", code])
            print(f"[SUCCESS] {device_id} Logged In!")
        else:
            print(f"[-] No SMS received for {phone}. Moving to next unit.")
            # Optional: Cancel order on 5sim to get refund
            requests.get(f"https://5sim.net/v1/user/cancel/{order_id}", headers=HEADERS)

if __name__ == "__main__":
    run_factory()
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
