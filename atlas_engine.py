import requests, subprocess, time, random

# SET THESE ONCE
TOKEN = AAFSOQAAvapTWrRgp48sZJnlEjERJhZGfhL9hcHr7RngUw
SENDER = "AtlasKlickBot"
PORTS = ["5554", "5556", "5558", "5560", "5562"] # Standard LDPlayer ADB ports

def register_unit(port):
    device = f"127.0.0.1:{port}"
    print(f"\n[#] Working on {device}...")
    
    # 1. Ask for number (You can automate this with a .txt list later)
    phone = input(f"Enter number for {device}: ")
    
    # 2. Trigger $0.01 Code
    res = requests.post("https://gatewayapi.telegram.org/sendVerificationMessage", 
        json={"phone_number": phone, "sender_username": SENDER, "code_length": 5},
        headers={"Authorization": f"Bearer {TOKEN}"}).json()
    
    if res.get('ok'):
        print(f"[!] Code sent! Check Fragment.")
        code = input("Enter Code: ")
        # 3. Type code into phone automatically
        subprocess.run(["adb", "-s", device, "shell", "input", "text", code])
        print(f"[SUCCESS] Unit {device} is logged in.")
    else:
        print(f"[ERROR] {res.get('error')}")

if __name__ == "__main__":
    for p in PORTS:
        register_unit(p)
