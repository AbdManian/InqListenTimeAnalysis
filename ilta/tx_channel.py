from .config import MainConfig
import random


class TxChannel:
    def __init__(self, cfg: MainConfig, node_id: int = 0):
        self.cfg = cfg
        self.cnt = 0
        self.node_id = node_id
        self.shuffle_channels = list(range(self.cfg.num_channels))

    def get_next_channel(self) -> list[int]:
        strategy = self.cfg.tx_strategy

        if strategy == "random":
            return self.node_id, self._get_next_random()

        if strategy == "shuffle":
            return self.node_id, self._get_next_shuffle()

        if strategy == "count":
            return self.node_id, self._get_next_count()

        raise ValueError(f'ERROR: Unknown tx-strategy "{strategy}"!')

    def _get_next_count(self) -> int:
        ret = self.cnt
        self.cnt = (self.cnt + 1) % self.cfg.num_channels
        return ret

    def _get_next_random(self) -> int:
        return random.randint(0, self.cfg.num_channels - 1)

    def _get_next_shuffle(self) -> int:
        if self.cnt == 0:
            random.shuffle(self.shuffle_channels)

        ret = self.shuffle_channels[self.cnt]
        self.cnt += 1

        if self.cnt >= self.cfg.num_channels:
            self.cnt = 0

        return ret
