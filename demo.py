from mlp import Mlp
import random
import pandas as pd
import numpy as np

training_xor = [
    {
        "input": [0, 0],
        "output": [0]
    },
    {
        "input": [1, 0],
        "output": [1]
    },
    {
        "input": [0, 1],
        "output": [1]
    },
    {
        "input": [1, 1],
        "output": [0]
    }
]

def xor():
    # Create a MLP with 2 input, a hidden layer with 2 nodes a single output node
    nn = Mlp(init_nodes=2)
    nn.add_layer(2)
    nn.add_layer(1)

    print("Training the network...")
    for i in range(20000):
        data = random.choice(training_xor)
        nn.train(data["input"], data["output"])
    # nn.save("xor.mlp")
    for i in range(2):
        for j in range(2):
            out_class, out_prob = nn.predict([i, j])
            print("Predicting XOR between {} and {} gave {} and the real is {} (Output: {:.2f})"
                  .format(i, j, out_prob > .5, bool(i) ^ bool(j), out_prob))


def ocr(training_population=5000, testing_population=1000):
    print("Loading data...")
    train = pd.read_csv("../datasets/mnist_train.csv")
    train = process_df(train)
    test_set = pd.read_csv("../datasets/mnist_test.csv")
    test_set = process_df(test_set)
    print("Loaded {} rows for training.".format(train.shape[0]))
    print("Loaded {} rows for testing.".format(test_set.shape[0]))
    nn = Mlp(init_nodes=784, learning_rate=.05)
    nn.add_layer(300)
    nn.add_layer(150, function="relu")
    nn.add_layer(10)

    print("Training the network with {} samples...".format(training_population))
    for i in range(training_population):
        data = train.sample(n=1)
        label = data["label"].tolist()[0]
        inputs = list(data.iloc[0, 1:])
        outputs = [0] * 10
        outputs[label] = 1
        nn.train(inputs, outputs)

    print("Trained successfully.")
    # nn.save("ocr.mlp")
    print("Testing with {} samples...".format(testing_population))
    c_m = np.zeros(shape=(10, 10))
    for i in range(testing_population):
        data = test_set.sample(n=1)
        inputs = list(data.iloc[0, 1:])
        label = data["label"].tolist()[0]
        out_class, out_prob = nn.predict(inputs)
        c_m[label][out_class] += 1

    print("Results:")

    correct_guesses = np.sum(np.diagonal(c_m))
    total_guesses = c_m.sum()
    accuracy = correct_guesses / total_guesses

    recall = 0
    precision = 0
    c_m_t = c_m.T

    for i in range(10):
        correct_guesses = c_m[i][i]
        total_row = np.sum(c_m[i])
        total_col = np.sum(c_m_t[i])
        recall += (correct_guesses / total_row) if total_row > 0 else 0
        precision += (correct_guesses / total_col) if total_col > 0 else 0
    
    recall = recall / 10
    precision = precision / 10

    print("\tRecall: {0:.2f}\n\tPrecision: {0:.2f}\n\tAccuracy: {0:.2f}".format(recall, precision, accuracy))


def filter_pixel(x):
    return x / 255


def process_df(df):
    labels = df["label"]
    df = df.drop(["label"], axis=1)
    df = df.apply(np.vectorize(filter_pixel))
    df = pd.concat([labels, df], axis=1)
    return df

ocr(training_population=50000, testing_population=5000)
# xor()
