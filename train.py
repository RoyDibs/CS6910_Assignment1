# -*- coding: utf-8 -*-
"""train_windb_file.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15Pwa5iSQwIemKrFJUhajPBtZUrkCnfsE
"""

import argparse
import wandb
import numpy as np
from tensorflow.keras.datasets import mnist, fashion_mnist
from AF import Sigmoid, tanh, identity, ReLU, softmax
from fwd_prop import ForwardPropagation
from initialise_weights import InitialiseParams
from optimiser import Optimiser
from back_prop import BackPropagation

def train_val_split(X, y, val_size, random_state=None):
    if random_state is not None:
        np.random.seed(random_state)

    num_samples = X.shape[0]
    num_val_samples = int(num_samples * val_size)

    indices = np.arange(num_samples)
    np.random.shuffle(indices)

    val_indices = indices[:num_val_samples]
    train_indices = indices[num_val_samples:]

    X_train, X_val = X[train_indices], X[val_indices]
    y_train, y_val = y[train_indices], y[val_indices]

    return X_train, X_val, y_train, y_val

def one_hot_encode(labels, num_classes):
    num_samples = len(labels)
    one_hot_labels = np.zeros((num_samples, num_classes))
    for i, label in enumerate(labels):
        one_hot_labels[i, label] = 1
    return one_hot_labels

def predict(X_test, parameters_trained, forward_propagator, layer_dims, activation_fn):
    AL, _ = forward_propagator.forward_propagation(X_test, layer_dims, parameters_trained, activation_fn)
    predictions = np.argmax(AL, axis=0)
    return predictions

def calculate_accuracy(predictions, y_test):
    correct_predictions = np.sum(predictions == y_test)
    total_predictions = len(y_test.T)
    accuracy = (correct_predictions / total_predictions) * 100
    return accuracy

# Command-line argument parsing
parser = argparse.ArgumentParser(description="Train neural network with specified hyperparameters.")
parser.add_argument("-wp", "--wandb_project", default="CS6910_Assignment_1", help="Project name used for Weights & Biases tracking")
parser.add_argument("-we", "--wandb_entity", default="dibakar", help="Wandb Entity used for Weights & Biases tracking")
parser.add_argument("-d", "--dataset", default="fashion_mnist", choices=["mnist", "fashion_mnist"], help="Dataset to use")
parser.add_argument("-e", "--epochs", type=int, nargs='+', default=[1], help="Number of epochs to train neural network")
parser.add_argument("-b", "--batch_size", type=int, nargs='+', default=[32], help="Batch size used to train neural network")
parser.add_argument("-l", "--loss", default="cross_entropy", choices=["mse", "cross_entropy"], help="Loss function")
parser.add_argument("-o", "--optimizer", nargs='+', default=['adam'], choices=["sgd", "momentum", "nestrov", "rmsprop", "adam", "nadam"], help="Optimizer")
parser.add_argument("-lr", "--learning_rate", type=float, nargs='+', default=[0.1], help="Learning rate")
parser.add_argument("-nhl", "--num_layers", type=int, nargs='+', default=[1], help="Number of hidden layers")
parser.add_argument("-sz", "--hidden_size", type=int, nargs='+', default=[4], help="Number of hidden neurons in a feedforward layer")
parser.add_argument("-a", "--activation", nargs='+', default=['ReLU'], choices=["identity", "sigmoid", "tanh", "ReLU"], help="Activation function")
parser.add_argument("-w_d", "--weight_decay", type=float, nargs='+', default=[0.0], help="Weight decay (alpha)")
parser.add_argument("-wi", "--weight_init", nargs='+', default=['random'], choices=["random", "xavier"], help="Weight initialization method (random or Xavier)")
parser.add_argument("-beta", "--beta", type=float, default=0.5, help="beta for momentum, nestrov and rmsprop")
parser.add_argument("-beta1", "--beta1", type=float, default=0.5, help="beta1 for adam and nadam")
parser.add_argument("-beta2", "--beta2", type=float, default=0.5, help="beta2 for adam and nadam")
parser.add_argument("-eps", "--epsilon", type=float, default=0.000001, help="Epsilon used by optimizers")
parser.add_argument("-swp_name", "--sweep_name", default="test of code", help="Name of the sweep")
parser.add_argument("-swp_count", "--sweep_count", default=2, help="Number of runs for sweep")

args = parser.parse_args()

sweep_config = {
    'method': 'bayes',
    'name' : args.sweep_name,
    'metric': {
      'name': 'val_accuracy',
      'goal': 'maximize'
    },
    'parameters': {
        'epochs': {
            'values': args.epochs
        },
         'hidden_layer':{
            'values': args.num_layers
        },
        'hidden_size':{
            'values': args.hidden_size
        },
        'weight_decay':{
            'values': args.weight_decay
        },
        'learning_rate':{
            'values': args.learning_rate
        },
        'optimizer':{
            'values': args.optimizer
        },
        'batch_size':{
            'values': args.batch_size
        },
        'weight_init': {
            'values': args.weight_init
        },
        'activation': {
            'values': args.activation
        },


    }
}

sweep_id = wandb.sweep(sweep=sweep_config, project=args.wandb_project)


# Data preprocessing
if args.dataset == "mnist":
    (x_train, y_train), (x_test, y_test) = mnist.load_data()
else:
    (x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()

# Define class labels
class_labels = {
    0: 'T-shirt/top', 1: 'Trouser', 2: 'Pullover', 3: 'Dress', 4: 'Coat',
    5: 'Sandal', 6: 'Shirt', 7: 'Sneaker', 8: 'Bag', 9: 'Ankle boot'
}

# Split data and preprocess
x_train, x_val, y_train, y_val = train_val_split(x_train, y_train, val_size=0.1, random_state=2)
x_train_scaled = x_train / 255.0
x_val_scaled = x_val / 255.0
x_test_scaled = x_test / 255.0

x_train_scaled = x_train_scaled.reshape(x_train_scaled.shape[0], x_train_scaled.shape[1]*x_train_scaled.shape[2]).T
x_val_scaled = x_val_scaled.reshape(x_val_scaled.shape[0], x_val_scaled.shape[1]*x_val_scaled.shape[2]).T
x_test_scaled = x_test_scaled.reshape(x_test_scaled.shape[0], x_test_scaled.shape[1]*x_test_scaled.shape[2]).T

# One-hot encode labels
class_num = len(np.unique(y_train))
y_train_one_hot = one_hot_encode(y_train, class_num).T
y_val_one_hot = one_hot_encode(y_val, class_num).T



def main():
    '''
    WandB calls main function each time with differnet combination.

    We can retrive the same and use the same values for our hypermeters.

    '''


    with wandb.init(project=args.wandb_project, entity=args.wandb_entity) as run:

        run_name ="d_{}_e_{}_bs_{}_loss_{}_op_{}_lr_{}_hl_{}_hsz_{}_ac_{}_aplha_{}_wi_{}_".format(args.dataset, wandb.config.epochs, wandb.config.batch_size,
                                                                                                args.loss, wandb.config.optimizer, wandb.config.learning_rate, wandb.config.hidden_layer, wandb.config.hidden_size,
                                                                                                wandb.config.activation, wandb.config.weight_decay, wandb.config.weight_init)
        wandb.run.name=run_name

        # Initialize parameters
        initializer = InitialiseParams(wandb.config.hidden_layer, wandb.config.hidden_size, x_train_scaled.shape[0], class_num)
        layer_dims = initializer.initialise_params()
        parameters_random = initializer.random_ini(layer_dims) if wandb.config.weight_init == "random" else initializer.xavier_ini(layer_dims)


        # Activation function
        activation_fn = ReLU() if wandb.config.activation == 'ReLU' else Sigmoid() if wandb.config.activation == 'sigmoid' else tanh() if wandb.config.activation == 'tanh' else identity()


        forward_propagator = ForwardPropagation()
        backpropagator = BackPropagation()
        optimiser = Optimiser()
        parameters = parameters_random
        optimizer_type = wandb.config.optimizer
        loss_function = args.loss
        batch_size = wandb.config.batch_size
        learning_rate = wandb.config.learning_rate
        beta = args.beta
        beta1 = args.beta1
        beta2 = args.beta2
        alpha = wandb.config.weight_decay
        max_epoch = wandb.config.epochs
        epsilon = args.epsilon

        # training procedure

        num_samples = x_train_scaled.shape[1]
        num_batches = num_samples // batch_size


        # Initialize velocities and moment
        velocities = {param_name: np.zeros_like(param) for param_name, param in parameters.items()}
        moment = {param_name: np.zeros_like(param) for param_name, param in parameters.items()} # for adam

        k_step = 3
        step = num_batches // k_step
        for epoch in range(max_epoch):
            for batch_idx in range(num_batches):
                start_idx = batch_idx * batch_size
                end_idx = start_idx + batch_size

                X_batch = x_train_scaled[:, start_idx:end_idx]
                y_batch = y_train_one_hot[:, start_idx:end_idx]

                # Forward propagation
                AL, caches = forward_propagator.forward_propagation(X_batch, layer_dims, parameters, activation_fn)

                # Compute loss
                if loss_function == 'cross_entropy':
                    cost = backpropagator.cross_entropy_loss(y_batch, AL, parameters, alpha)
                elif loss_function == 'mse':
                    cost = backpropagator.mean_squared_error_loss(y_batch, AL, parameters, alpha)
                else:
                    raise ValueError("Unsupported loss function")

                # Backward propagation
                grads = backpropagator.backward_propagation(y_batch, AL, caches, loss_function, parameters, alpha)

                # Update parameters using the specified optimizer
                if optimizer_type == 'sgd':
                    parameters = optimiser.stochastic_gradient_descent(parameters, grads, learning_rate, alpha)
                elif optimizer_type == 'momentum':
                    parameters = optimiser.momentum(parameters, grads, velocities, beta, learning_rate, alpha)
                elif optimizer_type == 'nestrov':
                    parameters = optimiser.nestrov(X_batch, y_batch, parameters, velocities, beta, learning_rate, loss_function, activation_fn, alpha, layer_dims)
                elif optimizer_type == 'rmsprop':
                    parameters = optimiser.rmsprop(parameters, grads, velocities, beta, learning_rate, alpha, epsilon)
                elif optimizer_type == 'adam':
                    parameters = optimiser.adam(parameters, grads, moment, velocities, beta1, beta2, learning_rate, alpha, epsilon)
                elif optimizer_type == 'nadam':
                    parameters = optimiser.nadam(parameters, grads, moment, velocities, beta1, beta2, learning_rate, alpha, epsilon)
                else:
                    raise ValueError("Unsupported optimizer type")



                #Calculate validation accuracy
                if batch_idx % step == 0:
                      # validation
                      AL_val, caches_val = forward_propagator.forward_propagation(x_val_scaled, layer_dims, parameters, activation_fn)

                      # Compute loss
                      if loss_function == 'cross_entropy':
                          val_loss = backpropagator.cross_entropy_loss(y_val_one_hot, AL_val, parameters, alpha)
                      elif loss_function == 'mse':
                          val_loss = backpropagator.mean_squared_error_loss(y_val_one_hot, AL_val, parameters, alpha)
                      else:
                          raise ValueError("Unsupported loss function")

                      predictions_val = predict(x_val_scaled, parameters, forward_propagator, layer_dims, activation_fn)
                      val_accuracy = calculate_accuracy(predictions_val, y_val)
                      wandb.log({'Epoch': epoch + 1, 'Train Loss': cost, 'val_loss': val_loss, 'val_accuracy': val_accuracy})


        # Test
        predictions = predict(x_test_scaled, parameters, forward_propagator, layer_dims, activation_fn)
        accuracy = calculate_accuracy(predictions, y_test)
        wandb.log({'Test_Accuracy': accuracy})

wandb.agent(sweep_id, function=main,count=args.sweep_count)
wandb.finish()

