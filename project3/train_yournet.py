"""
Train LeNet5

Example:
python train_yournet.py  --checkpoint-dir ./checkpoints/LeNet5/   --epoch-end 30   --device cpu

"""
import argparse
import os
import torch
from torch import nn
from torch.optim import optimizer
from torchvision import datasets, transforms
from models.YourNet import YourNet
# from models.LeNet5 import LeNet5 as YourNet
from eval.metrics import get_accuracy

# --------------- Arguments ---------------

parser = argparse.ArgumentParser()
parser.add_argument('--checkpoint-dir', type=str, required=True)
parser.add_argument('--last-checkpoint', type=str, default=None)
parser.add_argument('--device', type=str, choices=['cpu', 'cuda'], default='cpu')
parser.add_argument('--batch-size', type=int, default=64)
parser.add_argument('--epoch-start', type=int, default=0)
parser.add_argument('--epoch-end', type=int, required=True)

args = parser.parse_args()
# --------------- Loading ---------------

def train(model, train_loader, test_loader, optimizer,scheduler, loss_fn):
    # min_loss=100000000000
    best_acc=0
    for epoch in range(args.epoch_start, args.epoch_end):
        print(f"Epoch {epoch}\n-------------------------------")
        size = len(train_loader.dataset)
        model.train()
        for batch_idx, (X, y) in enumerate(train_loader):

            X, y = X.to(args.device), y.to(args.device)

            # Compute prediction error
            # if loss_fn == nn.CrossEntropyLoss() :
                
            pred_y = model(X)
            loss = loss_fn(pred_y,y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
                
            # else:
            #     pred_y = model(X)
            #     matrix=torch.zeros([len(pred_y),10]).to(args.device)
            #     for i in range(len(pred_y)):
            #         matrix[i,y[i]]=1
            #     matrix=matrix.float()
            #     pred_y=pred_y.float()
            #     loss = loss_fn(matrix,pred_y)
            #     optimizer.zero_grad()
            #     loss.backward()
            #     optimizer.step()

            if batch_idx % 100 == 0:
                loss, current = loss.item(), batch_idx * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
        scheduler.step()
        accuracy = get_accuracy(model, test_loader, args.device)
        print("Accuracy: %.3f}" % accuracy)
        if accuracy>best_acc:
            best_acc=accuracy
            torch.save(model.state_dict(), "./checkpoints/best.pth")
            
if __name__ == '__main__':

    train_loader = torch.utils.data.DataLoader(
        datasets.MNIST(root='./data', train=True, download=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                           ])),
        batch_size=args.batch_size, shuffle=True)

    test_loader = torch.utils.data.DataLoader(
        datasets.MNIST(root='./data', train=False,
                       transform=transforms.Compose([
                           transforms.ToTensor(),
                           transforms.Normalize((0.1307,), (0.3081,))
                       ])),
        batch_size=args.batch_size, shuffle=True)

    model = YourNet().to(device=args.device)

    if args.last_checkpoint is not None:
        model.load_state_dict(torch.load(args.last_checkpoint, map_location=args.device))

    loss_fn = nn.CrossEntropyLoss()
    
    optimizer = torch.optim.Adam(model.parameters(), lr=5e-3, weight_decay=1e-4)
    scheduler =torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=30, eta_min=0, last_epoch=-1)

    if not os.path.exists(args.checkpoint_dir):
        os.makedirs(args.checkpoint_dir)

    train(model, train_loader, test_loader, optimizer,scheduler, loss_fn)