"""
Maps an NFStream flow (with the InitWindowSize plugin) to the exact 78-feature
vector expected by best_model.joblib, in CICIDS2017 order.
"""
from init_window_plugin import InitWindowSize
import os
import joblib

FEATURE_NAMES = joblib.load(os.getenv("FEAT_PATH", "/home/b4der/nids-ai/ml/models/feature_names.joblib"))


def flow_to_features(flow) -> list:
    dur_s = max(flow.bidirectional_duration_ms / 1000.0, 1e-6)
    fwd_pkts = flow.src2dst_packets
    bwd_pkts = flow.dst2src_packets

    values = {
        "Destination Port": flow.dst_port,
        "Flow Duration": flow.bidirectional_duration_ms * 1000,
        "Total Fwd Packets": fwd_pkts,
        "Total Backward Packets": bwd_pkts,
        "Total Length of Fwd Packets": flow.src2dst_bytes,
        "Total Length of Bwd Packets": flow.dst2src_bytes,
        "Fwd Packet Length Max": flow.src2dst_max_ps,
        "Fwd Packet Length Min": flow.src2dst_min_ps,
        "Fwd Packet Length Mean": flow.src2dst_mean_ps,
        "Fwd Packet Length Std": flow.src2dst_stddev_ps,
        "Bwd Packet Length Max": flow.dst2src_max_ps,
        "Bwd Packet Length Min": flow.dst2src_min_ps,
        "Bwd Packet Length Mean": flow.dst2src_mean_ps,
        "Bwd Packet Length Std": flow.dst2src_stddev_ps,
        "Flow Bytes/s": flow.bidirectional_bytes / dur_s,
        "Flow Packets/s": flow.bidirectional_packets / dur_s,
        "Flow IAT Mean": flow.bidirectional_mean_piat_ms * 1000,
        "Flow IAT Std": flow.bidirectional_stddev_piat_ms * 1000,
        "Flow IAT Max": flow.bidirectional_max_piat_ms * 1000,
        "Flow IAT Min": flow.bidirectional_min_piat_ms * 1000,
        "Fwd IAT Total": flow.src2dst_duration_ms * 1000,
        "Fwd IAT Mean": flow.src2dst_mean_piat_ms * 1000,
        "Fwd IAT Std": flow.src2dst_stddev_piat_ms * 1000,
        "Fwd IAT Max": flow.src2dst_max_piat_ms * 1000,
        "Fwd IAT Min": flow.src2dst_min_piat_ms * 1000,
        "Bwd IAT Total": flow.dst2src_duration_ms * 1000,
        "Bwd IAT Mean": flow.dst2src_mean_piat_ms * 1000,
        "Bwd IAT Std": flow.dst2src_stddev_piat_ms * 1000,
        "Bwd IAT Max": flow.dst2src_max_piat_ms * 1000,
        "Bwd IAT Min": flow.dst2src_min_piat_ms * 1000,
        "Fwd PSH Flags": flow.src2dst_psh_packets,
        "Bwd PSH Flags": flow.dst2src_psh_packets,
        "Fwd URG Flags": flow.src2dst_urg_packets,
        "Bwd URG Flags": flow.dst2src_urg_packets,
        "Fwd Header Length": fwd_pkts * 20,
        "Bwd Header Length": bwd_pkts * 20,
        "Fwd Packets/s": fwd_pkts / dur_s,
        "Bwd Packets/s": bwd_pkts / dur_s,
        "Min Packet Length": flow.bidirectional_min_ps,
        "Max Packet Length": flow.bidirectional_max_ps,
        "Packet Length Mean": flow.bidirectional_mean_ps,
        "Packet Length Std": flow.bidirectional_stddev_ps,
        "Packet Length Variance": flow.bidirectional_stddev_ps ** 2,
        "FIN Flag Count": flow.bidirectional_fin_packets,
        "SYN Flag Count": flow.bidirectional_syn_packets,
        "RST Flag Count": flow.bidirectional_rst_packets,
        "PSH Flag Count": flow.bidirectional_psh_packets,
        "ACK Flag Count": flow.bidirectional_ack_packets,
        "URG Flag Count": flow.bidirectional_urg_packets,
        "CWE Flag Count": flow.bidirectional_cwr_packets,
        "ECE Flag Count": flow.bidirectional_ece_packets,
        "Down/Up Ratio": (bwd_pkts / fwd_pkts) if fwd_pkts > 0 else 0,
        "Average Packet Size": flow.bidirectional_bytes / flow.bidirectional_packets if flow.bidirectional_packets else 0,
        "Avg Fwd Segment Size": flow.src2dst_mean_ps,
        "Avg Bwd Segment Size": flow.dst2src_mean_ps,
        "Fwd Header Length.1": fwd_pkts * 20,
        "Fwd Avg Bytes/Bulk": 0, "Fwd Avg Packets/Bulk": 0, "Fwd Avg Bulk Rate": 0,
        "Bwd Avg Bytes/Bulk": 0, "Bwd Avg Packets/Bulk": 0, "Bwd Avg Bulk Rate": 0,
        "Subflow Fwd Packets": fwd_pkts,
        "Subflow Fwd Bytes": flow.src2dst_bytes,
        "Subflow Bwd Packets": bwd_pkts,
        "Subflow Bwd Bytes": flow.dst2src_bytes,
        "Init_Win_bytes_forward": max(flow.udps.init_win_fwd, 0),
        "Init_Win_bytes_backward": max(flow.udps.init_win_bwd, 0),
        "act_data_pkt_fwd": fwd_pkts,
        "min_seg_size_forward": 20,
        "Active Mean": 0, "Active Std": 0, "Active Max": 0, "Active Min": 0,
        "Idle Mean": 0, "Idle Std": 0, "Idle Max": 0, "Idle Min": 0,
    }

    return [float(values[name]) for name in FEATURE_NAMES]
