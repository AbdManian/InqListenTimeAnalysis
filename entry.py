import ilta



c = ilta.MainConfig()

c.num_channels = 4
c.num_nodes = 3
c.channel_per_ts = 4
c.tx_strategy = 'shuffle'
c.listen_duration = 1.3
c.rx_strategy = 'shuffle'


tx = ilta.TxChannelList(c)
rx = ilta.RxNodeList(c)

# rx = RxChannel(c, 49, 0)

# channel_visit = [0] * c.num_channels

# for i in range(10000):
#     node, channel = rx.get_next_listen_channel()
#     channel_visit[channel] += 1

#     # print(f'{channel}  ', end='')
#     # if i%10==9:
#     #     print()

# print(channel_visit)
# # tx = TxChannelList(c)


# for i in range(100):
#     print(tx.get_next_channel())

