NetPursuer - Network Monitoring Tool (v1.0.0)
====================================

## Description
NetPursuer is a network monitoring tool that scans your local network every 5 minutes to detect new devices. It creates a `detected_devices.pkl` file that remembers the devices detected on the first scan, preventing duplicate alerts for known devices. When a new device is detected, it sends an email alert containing the device's IP address and MAC address. This tool helps you stay informed about new connections and potential unauthorized access.

## Features
- Automated network scanning every 5 minutes
- Email notifications for newly detected devices
- Securely prompts for email password at runtime
- Uses `pickle` for persistent device tracking

## Requirements
Ensure you have the required dependencies installed:
```
pip install -r requirements.txt
```

## Usage
Run the program using:
```
python3 NetPursuer.py
```

### Running with Elevated Privileges
Since network scanning requires administrative privileges, you may need to run it with `sudo`:
```
sudo python3 NetPursuer.py
```

## Configuration
Modify the network subnet in the script before running:
- `ip_range`: Set this to match your local network (e.g., `192.168.1.0/24`).
Modify the following variables in the script before running:
- `SMTP_SERVER`: Your email provider's SMTP server
- `SMTP_PORT`: The SMTP port (e.g., 465 for SSL, 587 for TLS)
- `SENDER_EMAIL`: Your sender email address
- `RECEIVER_EMAIL`: The recipient email address for alerts

### Secure Email Password Entry
Instead of storing the password in the file, the program will:
- Prompt you for the password at runtime
- Use an environment variable (`EMAIL_PASSWORD`) if set

## Stopping the Program
To stop NetPursuer when running normally, press `CTRL+C` in the terminal.
