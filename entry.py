from ilta.config import MainConfig
from ilta.rx_node_list import RxNodeList
from ilta.tx_channel_list import TxChannelList
import numpy as np

c = MainConfig()

c.num_channels = 15
c.num_nodes = 5
c.channel_per_ts = 3
c.tx_strategy = "random"
c.listen_duration = 15
c.rx_strategy = "count"
c.rx_start_channel = "fixed"


tx = TxChannelList(c)
rx = RxNodeList(c)

test_cnt = (c.num_channels * c.num_nodes) * 10000

for i in range(test_cnt):
    node, channel = tx.get_next_channel()
    rx.process_received_channel(node, channel)


for i in range(c.num_nodes):
    channels = rx.get_rx_channel_info(i)
    dev = np.std(channels)
    total_sum = np.sum(channels)
    print(f"[{i}]: {channels} sum={total_sum} sd={dev}")
