from .rx_channel import RxChannel, MainConfig


class RxNode(RxChannel):
    def __init__(self, cfg: MainConfig, node_id: int = 0, start_channel: int = 0):
        RxChannel.__init__(self, cfg, node_id, start_channel)
        self.info_total_matched_node = (
            0  # Total number of matched node os sub-ts checked
        )
        self.info_total_matched_channel = 0
        self.info_channel = [0] * self.cfg.num_channels

    def process_received_channel(self, node_id: int, channel: int):
        _, cur_channel = self.get_next_listen_channel()

        if node_id != self.node_id:
            return

        self.info_total_matched_node += 1

        if cur_channel == channel:
            self.info_total_matched_channel += 1
            self.info_channel[channel] += 1

    def get_rx_channel_info(self):
        return self.info_channel
