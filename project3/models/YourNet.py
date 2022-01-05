from torch import nn
import torch.nn.functional as F

class YourNet(nn.Module):
    def __init__(self):
        super(YourNet, self).__init__()
        self.conv1 = nn.Conv2d(1, 4, 3)
        self.conv2 = nn.Conv2d(4, 5, 3)
        self.fc1 = nn.Linear(5 * 5 * 5, 10) 


    def forward(self, x):
        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2))
        x = F.max_pool2d(F.relu(self.conv2(x)), 2)
        x = x.view(-1, int(x.nelement() / x.shape[0]))
        x = self.fc1(x)
        return x
