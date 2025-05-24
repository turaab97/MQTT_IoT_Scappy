# MQTT_IoT_Scappy

IoT traffic simulation using Scappy 
Creating a Simulated Smart Home with Scapy

To give my students a hands-on IoT forensics lab without needing physical devices, I created a simulated network using Scapy. The idea was to mimic MQTT traffic between virtual smart home devices and a broker, then export the result as a PCAP file.

Here’s how I built it.

Step 1: Define the Devices
I started by defining a couple of virtual devices with MAC and IP addresses, topics, and payloads.

devices = [
    {"mac": "00:11:22:33:44:55", "ip": "192.168.1.10", "topic": "home/livingroom/light1", "payload": "ON"},
    {"mac": "00:11:22:33:44:66", "ip": "192.168.1.11", "topic": "home/garage/door", "payload": "OPEN"},
]
Step 2: Generate MQTT Packets
Using Scapy, I crafted basic TCP packets that simulate MQTT publish messages. For this example, the MQTT payload is just a string combining the topic and value.

from scapy.all import *

for device in devices:
    ether = Ether(src=device["mac"], dst="00:aa:bb:cc:dd:ee")
    ip = IP(src=device["ip"], dst="192.168.1.100")
    tcp = TCP(sport=12345, dport=1883, flags="PA", seq=1, ack=1)
    payload = f"{device['topic']}:{device['payload']}".encode()
    packet = ether / ip / tcp / Raw(load=payload)
    wrpcap("smart_home_iot.pcap", [packet], append=True)
Once the script is run, the network data is written to a PCAP file. Students can now open this pcap file in Wireshark or Network Miner for forensic analysis.

Analyzing the PCAP in Wireshark
After generating the traffic, students can load the smart_home_iot.pcap file in Wireshark and filter for MQTT-related traffic using

tcp.port == 1883

Why port 1883? It is because MQTT runs on TCP port 1883.

From there, students can:

Identify IP and MAC addresses of devices
Reconstruct a timeline of activity based on timestamps
Review which messages were sent to which topics
Investigate anomalies, like unauthorized access or unusual device behavior


Scapy is one of those tools that becomes more valuable the more you use it. Whether you’re teaching, researching, or working on a red or blue team, the ability to generate custom network traffic is incredibly useful.

By combining Scapy with MQTT, we can simulate smart home behavior in a repeatable way—perfect for building labs, testing detection rules, or deepening one's understanding of how IoT devices communicate.

A simple way to analyze IoT traffic.

Both the PY Script and Pcap are available in this repo.  Feel free to build upon this for educational purposes. 
