from dataclasses import dataclass

@dataclass
class MainConfig:
    num_nodes: int = 5
    num_channels: int = 15
    ts_duration: float = 0.03
    channel_per_ts: int = 3
    tx_strategy: str = 'count' # Values: count, shuffle, random
