# -*- coding: utf-8 -*-
"""forward_propagation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1okt79vmHh-7L3sTr597T3fcbsWIIbf6U
"""

import numpy as np
from AF import Sigmoid, tanh, identity, ReLU, softmax

class ForwardPropagation():
    def __init__(self, parameters, activation_fn):
        self.parameters = parameters
        self.activation_fn = activation_fn

    # def softmax(x):
    #     return np.exp(x) / np.sum(np.exp(x), axis=0)

    def forward_propagation(self, X, layer_dims):
        caches = []
        A = X
        L = len(layer_dims) - 1

        for l in range(1, L):
            A_prev = A
            W = self.parameters[f'W{l}']
            b = self.parameters[f'b{l}']
            Z = np.dot(W, A_prev) + b
            activation = self.activation_fn.value(Z)
            cache = (A_prev, W, b, Z, activation)
            caches.append(cache)
            A = activation

        # Output layer
        AL_prev = A
        WL = self.parameters[f'W{L}']
        bL = self.parameters[f'b{L}']
        ZL = np.dot(WL, AL_prev) + bL
        output = softmax().value(ZL)  # Using softmax activation for output layer

        cache = (AL_prev, WL, bL, ZL, output)
        caches.append(cache)

        return output, caches

