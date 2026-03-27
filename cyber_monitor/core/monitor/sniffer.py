from scapy.all import sniff
from .models import NetworkLog, SuspiciousActivity, Alert, Company
from .ml_model import train_model, detect, load_model
from collections import defaultdict
from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


channel_layer = get_channel_layer()


# -------------------------------
# Multi-tenant setup (demo)
# -------------------------------

COMPANY = Company.objects.first()  # Replace with dynamic company in production

# Load or train ML model for this company


ml_model = load_model(COMPANY)
if not ml_model:
    ml_model = train_model(COMPANY)

# -------------------------------
# Detection parameters
# -------------------------------

recent_ports = defaultdict(list)
TIME_WINDOW = timedeltadict(list)
PORT_THRESHOLD = 10


IP_COUNTER = defaultdict(list)
PACKET_THRESHOLD = 50

def send_ws_log(log_data, company):
    """
    Send log or alert to WebSocket for real-time dashboard.
    """

    async_to_sync(channel_layer.group_send)(
        f"logs_company_{company.id}",
        {
            "type": "send_log",
            "data": log_data
        }
    )


def process_packet(packet):
    now = datetime.now()

    if not packet.haslayer("IP"):
        return
    

    src = packet["IP"].src
    dst = packet["ip"].dst
    protocol = str(packet.proto)
    size = len(packet)

    """
    Save netork log

    """

    log = NetworkLog.objects.create(
        src_ip=src,
        dst_ip=dst,
        protocol=protocol,
        packet_size=size,
        Company=COMPANY
    )
    print(f"Captured: {src} → {dst} ({size} bytes)")
    
    # Push to Websocket
    send_ws_log({
        "type": "log",
        "src_ip": log.src_ip,
        "dst_ip": log.dst_ip,
        "protocol": log.protocol,
        "timestamp": str(log.timestamp)
    }, COMPANY)

    """
    PORT SCAN DETECTION
    """


    if packet.haslayer("TCP"):
        dst_port = packet["TCP"].dport
        recent_ports[src] = [p for p in recent_ports[src] if now - p[1] < TIME_WINDOW]
        recent_ports[src].append((dst_port, now))

        if len(recent_ports[src]) > PORT_THRESHOLD:
            alert = Alert.objects.create(
                src_ip=src,
                message=f"Port Scan Detected: {src}",
                severity="High",
                Company=COMPANY 
            )

    # -------------------------------
    # Port Scan Detection
    # -------------------------------

    if packet.haslayer("TCP"):
        dst_port = packet["TCP"].dport
        recent_ports[src] = [p for p in recent_ports[src] if now - p[1] < TIME_WINDOW]
        recent_ports[src].append((dst_port, now))

        if len(recent_ports[src]) > PORT_THRESHOLD:
            alert = Alert.objects.create(
                src_ip=src,
                message=f"⚠️ Port Scan Detected: {src}",
                severity="High",
                company=COMPANY
            )
            SuspiciousActivity.objects.create(
                src_ip=src,
                activity_type="Port Scan",
                details=f"Scanned ports: {[p[0] for p in recent_ports[src]]}",
                company=COMPANY
            )
            print(f"⚠️ Port Scan Detected from {src}")
            send_ws_log({
                "type": "alert",
                "message": alert.message,
                "severity": alert.severity,
                "timestamp": str(alert.timestamp)
            }, COMPANY)


    # ------------------------------
    # DOS DETECTION 
    # ------------------------------

    IP_COUNTER[src] = [t for t in IP_COUNTER[src] if now - t < TIME_WINDOW]
    IP_COUNTER[src].append(now)


    if len(IP_COUNTER[src]) > PACKET_THRESHOLD:
        alert = Alert.objects.create(
            src_ip=src,
            message=f"Potential DDos from {src}",
            severity="Critical",
            company=COMPANY
        )
        SuspiciousActivity.objects.create(
            src_ip=src,
            activity_type="DDoS",
            details=f"High packet rate: {len(IP_COUNTER[src])} pkts in {TIME_WINDOW}",
            company=COMPANY
        )

        print(f"⚠️ Potential DDoS from {src}")
        send_ws_log({
            "type": "alert",
            "message": alert.message,
            "severity": alert.severity,
            "timestamp": str(alert.timestamp)
        }, COMPANY)


    # -------------------------------
    # ML anomaly detection 
    # -------------------------------


    if detect(size, ml_model):
        alert = Alert.objects.create(
            src_ip=src,
            message=f" AI DETECTED ANOMALY frfom  {src}",
            severity="Medium",
            company=COMPANY
        )

        SuspiciousActivity.objects.create(
            src_ip=src,
            activity_type="ML Anomaly",
            details=f"Packet size: {size}",
            company=COMPANY
        )

        print(f"⚠️ AI DETECTED ANOMALY from  {src}")
        send_ws_log({
            "type": "alert",
            "message": alert.message,
            "severity": alert.severity,
            "timestamp": str(alert.timestamp)
        }, COMPANY)


def start_sniffing(interface=None):
    """
    Start sniffing packets on a given interface. 
    """
    if interface: 
        sniff(iface=interface, prn=process_packet, store=False)
    else:
        sniff(prn=process_packet, store=False)



