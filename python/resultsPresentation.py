import matplotlib.pyplot as plt
from matplotlib import style

style.use("ggplot")


def create_acc_loss_graph(modelName):
    contents = open(modelName, "r").read().split("\n")

    times = range(len(contents) - 1)
    accuracies = []
    losses = []

    val_accs = []
    val_losses = []

    for c in contents:
        if c:
            name, timestamp, acc, loss, val_acc, val_loss, epoch = c.split(",")
            accuracies.append(float(acc)*100)
            losses.append(float(loss))

            val_accs.append(float(val_acc)*100)
            val_losses.append(float(val_loss))

    fig = plt.figure()

    ax1 = plt.subplot2grid((2, 1), (0, 0))
    ax2 = plt.subplot2grid((2, 1), (1, 0), sharex=ax1)

    ax1.plot(times, accuracies, label="Training accuracy")
    ax1.plot(times, val_accs, label="Sample test accuracy")
    ax1.legend(loc=2)
    ax1.set(xlabel='Iteration', ylabel='Accuracy in %')
    ax2.plot(times, losses, label="Training loss")
    ax2.plot(times, val_losses, label="Test loss")
    ax2.legend(loc=2)
    ax2.set(xlabel='Iteration', ylabel='Loss')
    plt.show(block=True)


if __name__ == "__main__":
    from mainCuda import globNr
    modelName = 'model{}.log'.format(globNr.nr)
    create_acc_loss_graph(modelName)