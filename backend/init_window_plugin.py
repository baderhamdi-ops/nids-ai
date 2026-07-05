from nfstream import NFPlugin


def _parse_tcp_window(raw_ip_packet: bytes) -> int:
    """Extract the TCP window size from a raw IPv4 packet's bytes.
    Returns -1 if not IPv4/TCP or packet too short."""
    if not raw_ip_packet or len(raw_ip_packet) < 20:
        return -1
    version = raw_ip_packet[0] >> 4
    if version != 4:
        return -1  # skip IPv6 for now
    ihl_words = raw_ip_packet[0] & 0x0F
    ip_header_len = ihl_words * 4
    protocol = raw_ip_packet[9]
    if protocol != 6:  # not TCP
        return -1
    tcp_start = ip_header_len
    if len(raw_ip_packet) < tcp_start + 16:
        return -1
    window = int.from_bytes(raw_ip_packet[tcp_start + 14: tcp_start + 16], "big")
    return window


class InitWindowSize(NFPlugin):
    """Captures TCP window size on the first packet seen in each direction."""

    def on_init(self, packet, flow):
        w = _parse_tcp_window(packet.ip_packet)
        if packet.direction == 0:
            flow.udps.init_win_fwd = w
            flow.udps.init_win_bwd = -1
        else:
            flow.udps.init_win_bwd = w
            flow.udps.init_win_fwd = -1

    def on_update(self, packet, flow):
        w = _parse_tcp_window(packet.ip_packet)
        if packet.direction == 0 and flow.udps.init_win_fwd == -1:
            flow.udps.init_win_fwd = w
        elif packet.direction == 1 and flow.udps.init_win_bwd == -1:
            flow.udps.init_win_bwd = w
