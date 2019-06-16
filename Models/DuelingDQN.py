import torch
import torch.nn as nn
import torch.nn.functional as F

class Dueling_QNetwork(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed, fc1_units=64, fc2_units=64):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
            fc1_units (int): Number of nodes in first hidden layer
            fc2_units (int): Number of nodes in second hidden layer
        """
        super(Dueling_QNetwork, self).__init__()
        self.action_size = action_size
        self.seed = torch.manual_seed(seed)
        self.network = nn.Sequential(nn.Linear(state_size,fc1_units),
                                     nn.ReLU(),
                                     nn.Linear(fc1_units,fc2_units),
                                     nn.ReLU())
        self.advantage = nn.Sequential(nn.Linear(fc2_units,action_size))
        self.value = nn.Sequential(nn.Linear(fc2_units,1))

    def forward(self, state):
        x = self.network(state)
        value = self.value(x)
        value = value.expand(x.size(0), self.action_size)
        advantage = self.advantage(x)
        Q = value + advantage - advantage.mean()
        return Q
