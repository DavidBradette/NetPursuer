import time
import smtplib
from scapy.all import ARP, Ether, srp
import threading
import os
import pickle
import getpass

# Version number
__version__ = "1.0.0"

def display_intro():
    print(f"""
    ############################################################
    #                                                          #
    #                       NetPursuer                         #
    #                                                          #
    ############################################################
    
    Version: {__version__}

    NetPursuer is a network monitoring tool that scans your local 
    network every 5 minutes to detect new devices. When a new 
    device is detected, it sends an email alert containing the 
    device's IP address, and MAC address. The program continuously
    monitors your network to keep you informed about any new
    connections, helping to identify potential unauthorized
    access or devices.
    
    Author: David Bradette
    """)

    print(r"""

        |\      _,,,---,,_
       /,`.-'`'    -.  ;-;;,_
      |,4-  ) )-,_..;\ (  `'-'
     '---''(_/--'  `-'\_)

    """)
    time.sleep(2)

# Display author information and ASCII art
display_intro()

# Email configuration (MODIFY WITH YOUR EMAIL SERVER INFO)
SMTP_SERVER = "mail.example.com"
SMTP_PORT = 465
SENDER_EMAIL = "info@example.com"
RECEIVER_EMAIL = "info@example.com"

# Display email settings before asking for the password
print("If you need to update the email settings, please edit this file and modify the SMTP server, port, sender, or receiver email accordingly.")
print(f"SMTP Server: {SMTP_SERVER}")
print(f"SMTP Port: {SMTP_PORT}")
print(f"Sender Email: {SENDER_EMAIL}")
print(f"Receiver Email: {RECEIVER_EMAIL}")

# Securely prompt for email password
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD") or getpass.getpass("Enter your email password: ")

# File to store detected devices
DEVICE_FILE = "detected_devices.pkl"

# List to keep track of detected devices
detected_devices = set()

def load_detected_devices():
    global detected_devices
    if os.path.exists(DEVICE_FILE):
        with open(DEVICE_FILE, "rb") as f:
            detected_devices = pickle.load(f)

def save_detected_devices():
    with open(DEVICE_FILE, "wb") as f:
        pickle.dump(detected_devices, f)

def send_email(new_device):
    program_name = "NetPursuer"
    subject = f"New Device Detected on the Network"
    body = (
        f"A new device has been detected by {program_name}:\n\n"
        f"IP Address: {new_device['ip']}\n"
        f"MAC Address: {new_device['mac']}\n\n"
    )

    email_message = f"Subject: {subject}\n\n{body}"

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_message)
            print(f"Email sent to {RECEIVER_EMAIL} for new device: {new_device['ip']}")
    except Exception as e:
        print(f"Failed to send email using TLS: {e}")
        try:
            with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email_message)
                print(f"Email sent to {RECEIVER_EMAIL} for new device: {new_device['ip']}")
        except Exception as e:
            print(f"Failed to send email using SSL: {e}")

def scan_network(ip_range="192.168.0.0/24"):
    global detected_devices
    arp = ARP(pdst=ip_range)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    new_devices = []
    for sent, received in result:
        device = {'ip': received.psrc, 'mac': received.hwsrc}
        device_identifier = f"{device['ip']}-{device['mac']}"

        if device_identifier not in detected_devices:
            new_devices.append(device)

    if new_devices:
        for new_device in new_devices:
            detected_devices.add(f"{new_device['ip']}-{new_device['mac']}")
            send_email(new_device)

    save_detected_devices()

def scheduled_scan(interval=300):
    first_scan = True
    while True:
        print("Scanning network...")
        if not first_scan:
            scan_network()
        else:
            scan_network()
            first_scan = False
        time.sleep(interval)

# Load previously detected devices
load_detected_devices()

# Start the scheduled scan in a separate thread
scan_thread = threading.Thread(target=scheduled_scan)
scan_thread.daemon = True
scan_thread.start()

# Keep the main program running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping the network scan.")
