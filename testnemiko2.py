from netmiko import ConnectHandler
import time

print("welcome to gosas_network: saving lives via coding")

# Connect to Router1 (jump host)
device = {
    "device_type": "cisco_ios",
    "host": "192.168.17.133",
    "username": "gosas",
    "password": "gosas123",
    "secret": "gosas123"
}

conn = ConnectHandler(**device)
conn.enable()

routers = ["2.2.2.2", "3.3.3.3", "4.4.4.4"]

for ip in routers:
    print(f"\n=== Connecting to {ip} via Router1 ===")

    # SSH to internal router
    output = conn.send_command_timing(f"ssh -l gosas {ip}")
    
    if "Password" in output:
        output += conn.send_command_timing("gosas123")
    
    # Now we are on the internal router
    output += conn.send_command_timing("show ip int brief")
    print(output)

    # Exit back to Router1
    conn.send_command_timing("exit")
    time.sleep(1)

conn.disconnect()