"""DQN neural network for Snake."""

import torch.nn as nn


class DQNNetwork(nn.Module):
    def __init__(self, input_size: int, output_size: int, hidden_size: int = 128):
        super().__init__()
        raise NotImplementedError

    def forward(self, x):
        raise NotImplementedError
