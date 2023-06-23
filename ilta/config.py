from dataclasses import dataclass
from typing import Literal

@dataclass
class MainConfig:
    num_nodes: int = 5
    num_channels: int = 15
    ts_duration: float = 0.03
    channel_per_ts: int = 3
    tx_strategy: Literal['count', 'shuffle', 'random'] = 'count'
    listen_duration: float = 15
    rx_strategy: Literal['count', 'shuffle', 'random'] = 'count'
    rx_start_channel: Literal['fixed', 'count', 'random'] = 'fixed'