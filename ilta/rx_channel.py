from .config import MainConfig
import random


class RxChannel:
    def __init__(self, cfg: MainConfig, node_id: int = 0, start_channel: int = 0):
        self.cfg = cfg
        self.cur_channel = start_channel
        self.node_id = node_id
        self.cur_time = 0
        self.cur_listen_time = int(self.cfg.listen_duration)
        self.listen_frac = self.cfg.listen_duration - self.cur_listen_time
        self.listen_channels_frac = [0.0] * self.cfg.num_channels
        
        self.shuffle_cnt = self.cfg.num_channels
        self.shuffle_channels = list(range(self.cfg.num_channels))

        strategy = self.cfg.rx_strategy
        if strategy == 'shuffle':
            self._calc_next_channel_shuffle()

        if strategy == 'random':
            self._calc_next_channel_random()
        
        self._update_channel_listen_time()

    def get_next_listen_channel(self) -> tuple[int, int]:
        ret = self.node_id, self.cur_channel

        self.cur_time += 1
        if self.cur_time>= self.cur_listen_time:
            self.cur_time = 0
            self.cur_listen_time = int(self.cfg.listen_duration)
            
            strategy = self.cfg.rx_strategy

            if strategy == 'count':
                self._calc_next_channel_count()
            elif strategy == 'random':
                self._calc_next_channel_random()
            elif strategy == 'shuffle':
                self._calc_next_channel_shuffle()
            else:
                raise ValueError(f'ERROR: Invalid rx strategy "{strategy}"!')
           
            # Calculate next channel
            self._update_channel_listen_time()

        return ret
    
    def _calc_next_channel_count(self):
        self.cur_channel = (self.cur_channel + 1) % self.cfg.num_channels

    def _calc_next_channel_random(self):
        self.cur_channel = random.randint(0, self.cfg.num_channels-1)
    
    def _calc_next_channel_shuffle(self):
        self.shuffle_cnt += 1
        if self.shuffle_cnt>=self.cfg.num_channels:
            random.shuffle(self.shuffle_channels)
            self.shuffle_cnt = 0

        self.cur_channel = self.shuffle_channels[self.shuffle_cnt]

    def _update_channel_listen_time(self):
        cur_frac = self.listen_channels_frac[self.cur_channel] + self.listen_frac
        if cur_frac > 1.0:
            cur_frac -= 1.0
            self.cur_listen_time += 1
        self.listen_channels_frac[self.cur_channel] = cur_frac
           