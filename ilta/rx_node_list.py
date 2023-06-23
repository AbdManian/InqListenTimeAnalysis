from .rx_node import RxNode
from .config import MainConfig
import random


class RxNodeList:
    def __init__(self, cfg: MainConfig):
        self.cfg = cfg
        self.nodes = [
            RxNode(self.cfg, i, self._get_start_channel(i))
            for i in range(self.cfg.num_nodes)
        ]
        self.info_total_channel = 0

    def process_received_channel(self, node_index, channel):
        for node in self.nodes:
            node.process_received_channel(node_index, channel)
        
        self.info_total_channel += 1

    def _get_start_channel(self, index):
        strategy = self.cfg.rx_start_channel

        if strategy == "fixed":
            return 0

        if strategy == "count":
            return index % self.cfg.num_channels

        if strategy == "random":
            return random.randint(0, self.cfg.num_channels - 1)

        raise ValueError(f"Invalid rx start channel strategy {strategy}")
