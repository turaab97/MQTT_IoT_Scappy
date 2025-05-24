from scapy.all import *
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
from datetime import datetime

# Create a simulated MQTT publish packet for 3 IoT devices
def create_mqtt_pcap():
    packets = []
    
    devices = [
        {"mac": "00:11:22:33:44:55", "ip": "192.168.1.10", "topic": "home/livingroom/light1", "payload": "ON"},
        {"mac": "00:11:22:33:44:66", "ip": "192.168.1.11", "topic": "home/garage/door", "payload": "OPEN"},
        {"mac": "00:11:22:33:44:77", "ip": "192.168.1.12", "topic": "home/kitchen/thermostat", "payload": "22C"},
    ]
    
    broker_ip = "192.168.1.100"
    broker_mac = "00:aa:bb:cc:dd:ee"
    timestamp = int(datetime.now().timestamp())

    for device in devices:
        ether = Ether(src=device["mac"], dst=broker_mac)
        ip = IP(src=device["ip"], dst=broker_ip)
        tcp = TCP(sport=12345, dport=1883, flags="PA", seq=1, ack=1)
        mqtt_payload = f"{device['topic']}:{device['payload']}".encode()
        packet = ether / ip / tcp / Raw(load=mqtt_payload)
        packet.time = timestamp
        packets.append(packet)
        timestamp += 1

    wrpcap("smart_home_iot.pcap", packets)
    print("✅ PCAP file saved as smart_home_iot.pcap")

create_mqtt_pcap()

