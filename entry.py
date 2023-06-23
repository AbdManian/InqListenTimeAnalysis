from ilta.tx_channel_list import TxChannelList
from ilta import MainConfig

c = MainConfig()

c.num_channels = 10
c.num_nodes = 3
c.channel_per_ts = 4
c.tx_strategy = 'shuffle'

tx = TxChannelList(c)


for i in range(100):
    print(tx.get_next_channel())

