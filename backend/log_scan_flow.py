import sys, json
sys.path.insert(0, "/home/b4der/nids-ai/backend")
from nfstream import NFStreamer
from init_window_plugin import InitWindowSize
from feature_mapper import flow_to_features, FEATURE_NAMES

TARGET_IP = "192.168.100.1"  # change to whichever you scan next

streamer = NFStreamer(source="wlan0", statistical_analysis=True,
                       udps=InitWindowSize(), idle_timeout=10, active_timeout=60)

print(f"[NIDS] Watching for flows to {TARGET_IP} ... run your nmap scan now.")
for flow in streamer:
    if flow.dst_ip == TARGET_IP:
        vec = flow_to_features(flow)
        print(f"\nFlow: {flow.src_ip} -> {flow.dst_ip}:{flow.dst_port} | pkts: {flow.bidirectional_packets}")
        for name, val in zip(FEATURE_NAMES, vec):
            print(f"  {name:<28} {val}")
        break  # just grab one flow for comparison
