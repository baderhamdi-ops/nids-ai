import sys
import requests
sys.path.insert(0, "/home/b4der/nids-ai/backend")

from nfstream import NFStreamer
from init_window_plugin import InitWindowSize
from feature_mapper import flow_to_features

API_URL = "http://localhost:8000/api/predict"
INTERFACE = "wlan0"

def main():
    print(f"[NIDS] Starting live capture on {INTERFACE}... (Ctrl+C to stop)")
    streamer = NFStreamer(
        source=INTERFACE,
        statistical_analysis=True,
        udps=InitWindowSize(),
        idle_timeout=15,   # shorter timeout for faster testing feedback
        active_timeout=120,
    )

    for flow in streamer:
        try:
            features = flow_to_features(flow)
        except Exception as e:
            print(f"[NIDS] Feature extraction failed: {e}")
            continue

        payload = {
            "features": features,
            "src_ip": flow.src_ip,
            "dst_ip": flow.dst_ip,
            "dst_port": flow.dst_port,
            "protocol": "TCP" if flow.protocol == 6 else ("UDP" if flow.protocol == 17 else str(flow.protocol)),
        }

        try:
            resp = requests.post(API_URL, json=payload, timeout=3)
            resp.raise_for_status()
            result = resp.json()
        except Exception as e:
            print(f"[NIDS] API call failed: {e}")
            continue

        tag = "🔴 ATTACK" if result["is_attack"] else "🟢 benign"
        print(f"{tag} | {flow.src_ip} -> {flow.dst_ip}:{flow.dst_port} | "
              f"{result['prediction']} (conf={result['confidence']}) | severity={result['severity']}")

if __name__ == "__main__":
    main()
