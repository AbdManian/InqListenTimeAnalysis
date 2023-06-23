from ilta.config import MainConfig
from ilta.rx_node_list import RxNodeList
from ilta.tx_channel_list import TxChannelList
import numpy as np
import argparse


def create_arg():
    parser = argparse.ArgumentParser(description="Inq Listen Time Analysis")
    parser.add_argument(
        "-n",
        dest="num_nodes",
        metavar="NUM",
        help="Number of nodes",
        type=int,
        choices=range(1, 10),
        default=3,
    )

    parser.add_argument(
        "-c",
        dest="num_channels",
        metavar="CHANNELS",
        help="Number of channels",
        type=int,
        choices=range(13, 64),
        default=15,
    )

    parser.add_argument(
        "-t",
        help="Number of channels per ts",
        dest="channel_per_ts",
        metavar="NUM",
        type=int,
        choices=range(2, 10),
        default=3,
    )

    parser.add_argument(
        "-tx",
        help='TX channel switching strategy. "count": iterate over channels "shuffle": shuffle channels "random": select channels randomly',
        dest="tx_strategy",
        metavar="STRATEGY",
        choices=["count", "shuffle", "random"],
        default="count",
    )

    parser.add_argument(
        "-rx",
        help='RX channel switching strategy. Check tx strategy for values}',
        dest="rx_strategy",
        metavar="STRATEGY",
        choices=["count", "shuffle", "random"],
        default="count",
    )

    parser.add_argument(
        "-l",
        help="Listen duration for rx nodes. Default determined by number of channels",
        dest="listen_duration",
        metavar="DURATION",
        default=-1.0,
        type=float,
    )

    parser.add_argument(
        "-sc",
        help='Start channel selection in rx-nodes. "fixed":start from 0  "count":Iterate channels for each node "random":select start channel randomly',
        dest="rx_start_channel",
        metavar="STRATEGY",
        choices=["fixed", "count", "random"],
        default="fixed",
    )

    parser.add_argument(
        '-r',
        help='Number of rounds to perform simulation. Each round iterates over all nodes and channels',
        dest='test_count',
        metavar='NUM',
        type=int,
        default=10000
    )

    arg = parser.parse_args()
    return arg

def create_config(args):
    config = MainConfig()
    config.num_nodes = args.num_nodes
    config.num_channels = args.num_channels
    config.channel_per_ts = args.channel_per_ts
    config.tx_strategy = args.tx_strategy
    config.rx_strategy = args.rx_strategy

    listen_duration = args.listen_duration
    if listen_duration <= 0.0:
        listen_duration = config.num_channels

    config.listen_duration = listen_duration
    config.rx_start_channel = args.rx_start_channel
    return config

def show_config(config: MainConfig, test_count:int):
    print(f'Number of Nodes       : {config.num_nodes}')
    print(f'Number of Channels    : {config.num_channels}')
    print(f'Channels per TS       : {config.channel_per_ts}')
    print(f'TX Strategy           : {config.tx_strategy}')
    print(f'RX Strategy           : {config.rx_strategy}')
    print(f'RX Node Start Channel : {config.rx_start_channel}')
    print(f'Test count            : {test_count}')





def main():
    args = create_arg()
    config = create_config(args)

    show_config(config, args.test_count)

    tx = TxChannelList(config)
    rx = RxNodeList(config)
    test_cnt = (config.num_channels * config.num_nodes) * args.test_count

    for i in range(test_cnt):
        node, channel = tx.get_next_channel()
        rx.process_received_channel(node, channel)


    for i in range(config.num_nodes):
        channels = rx.get_rx_channel_info(i)
        dev = np.std(channels)
        total_sum = np.sum(channels)
        print(f"[{i}]: {channels} sum={total_sum} sd={dev}")


if __name__ == "__main__":
    main()
