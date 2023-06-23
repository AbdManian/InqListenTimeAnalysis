from .tx_channel import TxChannel
from .config import MainConfig


class TxChannelList:
    def __init__(self, cfg: MainConfig) -> None:
        self.cfg = cfg
        self.nodes = [TxChannel(cfg, i) for i in range(self.cfg.num_nodes)]
        self.cur_node = 0
        self.cur_channel = 0

    def _get_cur_node(self):
        return self.nodes[self.cur_node]

    def _next_channel(self):
        self.cur_channel += 1
        if self.cur_channel >= self.cfg.channel_per_ts:
            self.cur_channel = 0
            return True
        return False

    def _next_node(self):
        self.cur_node += 1
        if self.cur_node >= self.cfg.num_nodes:
            self.cur_node = 0
            return True
        return False

    def get_next_channel(self) -> tuple[int, int]:
        ret = self._get_cur_node().get_next_channel()

        if self._next_channel():
            self._next_node()
        return ret
