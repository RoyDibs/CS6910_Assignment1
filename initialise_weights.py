# -*- coding: utf-8 -*-
"""initialise weights.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1okt79vmHh-7L3sTr597T3fcbsWIIbf6U
"""

import numpy as np

class InitialiseParams:
    def __init__(self, num_layers, hidden_size, input_features, num_classes):
        self.num_layers = num_layers
        self.hidden_size = hidden_size
        self.input_features = input_features
        self.num_classes = num_classes

    def initialise_params(self):
        # Create a list of layer dimensions [input_features, hidden_size, ..., hidden_size, num_classes]
        layer_dim = [self.input_features]
        for _ in range(self.num_layers):
            layer_dim.append(self.hidden_size)
        layer_dim.append(self.num_classes)
        return layer_dim

    def random_ini(self, layer_dim):
        parameters = {}
        np.random.seed(10)
        num_layers = len(layer_dim)
        for l in range(1, num_layers):
            parameters[f'W{l}'] = np.random.randn(layer_dim[l], layer_dim[l-1]) * 0.01
            parameters[f'b{l}'] = np.zeros((layer_dim[l], 1))
        return parameters

    def xavier_ini(self, layer_dim):
        parameters = {}
        np.random.seed(10)
        num_layers = len(layer_dim)
        for l in range(1, num_layers):
            parameters[f'W{l}'] = np.random.randn(layer_dim[l], layer_dim[l-1]) * np.sqrt(1 / layer_dim[l-1])
            parameters[f'b{l}'] = np.zeros((layer_dim[l], 1))
        return parameters