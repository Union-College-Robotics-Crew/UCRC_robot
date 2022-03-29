import rotaryio
import board


class Encoder:

    def __init__(self, enc_config):
        self.encoder = enc_config
        self.prev_count = 0

    
    def get_position(self):
        return self.encoder.position / 3


    def __repr__(self):
        return str(self.get_position())
