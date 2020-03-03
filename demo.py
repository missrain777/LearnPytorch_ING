import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

#Load and normalizing the CIFAR10 training and test datasets using torchvision
transform = transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
trainset = torchvision.datasets.CIFAR10(root='./data', train=True,download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=4,shuffle=True, num_workers=2)
testset = torchvision.datasets.CIFAR10(root='./data', train=False,download=True, transform=transform)
testloader = torch.utils.data.DataLoader(testset, batch_size=4,shuffle=False, num_workers=2)
classes = ('plane', 'car', 'bird', 'cat','deer', 'dog', 'frog', 'horse', 'ship', 'truck')

#Define a Convolutional Neural Network
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(16*5*5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)
       
    def forward(self, x): 
        x = self.pool(F.relu(self.conv1(x))) 
        x = self.pool(F.relu(self.conv2(x))) 
        x = x.view(-1, 16 * 5 * 5) 
        x = F.relu(self.fc1(x)) 
        x = F.relu(self.fc2(x)) 
        x = self.fc3(x) 
        return x


net = Net()
#Define a Loss function and optimize
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9) 

PATH = './cifar_net.pth'
#Train the network
def train(epochs):
    for epoch in range(epochs):
        running_loss = 0.0 
        for i, data in enumerate(trainloader, 0): 
            # get the inputs 
            inputs, labels = data 
            # zero the parameter gradients 
            optimizer.zero_grad() 
            # forward + backward + optimizer
            outputs = net(inputs) 
            loss = criterion(outputs, labels) 
            loss.backward() 
            optimizer.step() 
            # print statistics 
            running_loss += loss.item()
            if i % 2000 == 1999: 
                # print every 2000 mini-batches 
                print('[%d, %5d] loss: %.5f' % (epoch + 1, i + 1, running_loss / 2000)) 
                running_loss = 0.0
    print('Finished Training')
    torch.save(net.state_dict(), PATH)


def Test():
    #Load back in our saved model 
    net.load_state_dict(torch.load(PATH))
    #Let us look at how the network performs on the whole dataset.
    correct = 0
    total = 0
    class_correct = list(0. for i in range(10))
    class_total = list(0. for i in range(10))
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            outputs = net(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            c = (predicted == labels).squeeze()
            for i in range(4):
                label = labels[i]
                class_correct[label] += c[i].item()
                class_total[label] += 1
    print('Accuracy of the network on the 10000 test images: %d %%' % (100 * correct / total))
    for i in range(10):
        print('Accuracy of %5s : %2d %%' % (classes[i], 100 * class_correct[i] / class_total[i]))


if __name__ == "__main__":
    #If you have trained your net,you won't need to train the net again.
    #epochs = 10
    #train(epochs)
    Test()
