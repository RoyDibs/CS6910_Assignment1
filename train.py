# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QzCshBTjXnZLv-G93mJstIPizJt6Jrkd
"""

import numpy as np

def train(X_train, x_val, y_train, y_val, parameters_random, activation_fn, layer_dims, forward_propagator, backpropagator, optimiser, optimizer_type, loss_function, max_epoch, batch_size, learning_rate, beta, beta1, beta2):
    num_samples = X_train.shape[1]
    num_batches = num_samples // batch_size

    # Get initial parameters from forward propagator
    parameters = parameters_random

    # Initialize velocities and moment
    velocities = {param_name: np.zeros_like(param) for param_name, param in parameters.items()}
    moment = {param_name: np.zeros_like(param) for param_name, param in parameters.items()} # for adam

    for epoch in range(max_epoch):
        for batch_idx in range(num_batches):
            start_idx = batch_idx * batch_size
            end_idx = start_idx + batch_size

            X_batch = X_train[:, start_idx:end_idx]
            y_batch = y_train[:, start_idx:end_idx]

            # Forward propagation
            AL, caches = forward_propagator.forward_propagation(X_batch, layer_dims, parameters, activation_fn)

            # Compute loss
            if loss_function == 'cross_entropy':
                cost = backpropagator.cross_entropy_loss(y_batch, AL)
            elif loss_function == 'mse':
                cost = backpropagator.mean_squared_error_loss(y_batch, AL)
            else:
                raise ValueError("Unsupported loss function")

            # Backward propagation
            grads = backpropagator.backward_propagation(y_batch, AL, caches, loss_function)

            # Update parameters using the specified optimizer
            if optimizer_type == 'sgd':
                parameters = optimiser.stochastic_gradient_descent(parameters, grads, learning_rate)
            elif optimizer_type == 'momentum':
                parameters = optimiser.momentum(parameters, grads, velocities, beta, learning_rate)
            elif optimizer_type == 'nestrov':
                parameters = optimiser.nestrov(X_batch, y_batch, parameters, velocities, beta, learning_rate, loss_function, activation_fn)
            elif optimizer_type == 'rmsprop':
                parameters = optimiser.rmsprop(parameters, grads, velocities, beta, learning_rate)
            elif optimizer_type == 'adam':
                parameters = optimiser.adam(parameters, grads, moment, velocities, beta1, beta2, learning_rate)
            elif optimizer_type == 'nadam':
                parameters = optimiser.nadam(parameters, grads, moment, velocities, beta1, beta2, learning_rate)
            else:
                raise ValueError("Unsupported optimizer type")

            # validation
            AL_val, caches_val = forward_propagator.forward_propagation(x_val, layer_dims, parameters, activation_fn)

            # Compute loss
            if loss_function == 'cross_entropy':
                cost_val = backpropagator.cross_entropy_loss(y_val, AL_val)
            elif loss_function == 'mse':
                cost_val = backpropagator.mean_squared_error_loss(y_val, AL_val)
            else:
                raise ValueError("Unsupported loss function")

            if batch_idx % batch_size == 0:
                print(f"Epoch {epoch+1}/{max_epoch}, Batch {batch_idx+1}/{num_batches}, Loss: {cost}, validation: {cost_val}")

    return parameters