import argparse
def main():
    parser = argparse.ArgumentParser(description='Spektral Argument Parser')
    parser.add_argument('--epochs', type=int, default=100, help= 'number of epochs')
    parser.add_argument('--batch_size', type=int, default=256, help= 'batch size')
    parser.add_argument('--amount', type=int, default=133000, help= 'number of molecules in dataset')
    parser.add_argument('--learning_rate', type=float, default=1e-3, help='learning rate')

    args = parser.parse_args()
    return args


args = main()
epochs = args.epochs
batch_size = args.batch_size
amount = args.amount
learning_rate = args.learning_rate

print("Num epochs: {0} \n Batch Size: {1} \n Amount: {2} \n Learning Rate: {3} ".format(epochs,batch_size, amount, learning_rate))