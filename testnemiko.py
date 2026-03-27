from netmiko import ConnectHandler

router = {
    "device_type": "cisco_ios",
    "host": "192.168.17.133",
    "username": "gosas",
    "password": "gosas123",
    "secret": "gosas123"
}


test_conn = ConnectHandler(**router)
test_conn.enable()

loopback_ip = "1.1.1.1"
loopback_command = [
    f"interface loopback0",
    f"ip address {loopback_ip} 255.255.255.255",
    "no shutdown",
    "exit"   
]

print("loopback configuration......")
output = test_conn.send_config_set(loopback_command)
print(output)

ospf_command = [
    "router ospf 1",
    f"router-id {loopback_ip}",
    "network 192.168.17.0 0.0.0.255 area 0",
    "network 4.1.1.1 0.0.0.3 area 0",
    "exit"
]

print("ospf configuration.....")
output2 = test_conn.send_config_set(ospf_command)
print(output2)



save = test_conn.save_config()
print(f"configuration saved: \n{save}")

test_conn.disconnect()
print("OSPF AND LOOPBACK CONFIGURED SUCCESSFULLY")