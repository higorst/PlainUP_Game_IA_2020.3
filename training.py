from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader

# File with positions and distances
file = open('data_generate_x_y.txt', 'r');

data_file = file.readlines();
values = [];
for line in data_file:
    dist_x, dist_y, tree_x, tree_y, action = line.split('/');
    values.append([dist_x, dist_y, tree_x, tree_y, action[0]])

file.close()
file_train_value = open('data_trainer.txt', 'a');
ds = SupervisedDataSet(4, 1)
for data in values:
    ds.addSample((data[0], data[1],data[2], data[3]),(data[4]));

rn = buildNetwork(4, 20, 1, bias=True)
trainer = BackpropTrainer(rn, ds)
for i in range(100):
    print(i)
    train = trainer.train()
    file_train_value.write(str(train)+'\n');
    
NetworkWriter.writeToFile(rn, 'filename6.xml')
file_train_value.close()