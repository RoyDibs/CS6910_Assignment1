# CS6910_Assignment1 Repository

Welcome to the CS6910_Assignment1 repository! This repository contains the Python files used to generate the results presented in the accompanying report. For detailed insights, please refer to the report available [here](https://api.wandb.ai/links/dibakar/s0xfcb15).

### Contents Overview:

1. **AF.py**: 
   - This file encompasses implementations of various activation functions used in neural networks.

2. **initialize_weights.py**: 
   - It furnishes functions for initializing weights, offering choices such as random initialization or Xavier initialization.

3. **fwd_prop.py**: 
   - Here lies a class dedicated to forward propagation in neural networks, a pivotal step in processing input data through the network layers.

4. **back_prop.py**: 
   - This file hosts a class essential for backpropagation, a fundamental technique in training neural networks by calculating gradients and updating weights.

5. **optimizer.py**: 
   - A comprehensive suite of classes implementing diverse optimization algorithms:
     - Stochastic Gradient Descent: 'sgd'
     - Momentum-based Gradient Descent: 'moment'
     - Nesterov Accelerated Gradient Descent: 'nesterov'
     - RMSprop: 'rmsprop'
     - Adam: 'adam'
     - Nadam: 'nadam'

6. **train.py**: 
   - The backbone of the training process, this file orchestrates the entire training workflow. It can initiate any sweep using the Bayesian search method for a specified count. You can customize the sweep using the arguments '-swp_name' and '-swp_count', setting the sweep name and the number of counts for the sweep to execute.

### Jupyter Notebooks:

1. **Question1**: 
   - This notebook is dedicated to data collection and visualization, producing images for each class.
   
2. **Question2**: 
   - Explore this notebook for functions and implementations of forward propagation, crucial for feeding data through the network layers.

3. **Question3**: 
   - Dive into this notebook for functions and implementations of backward propagation with various optimizers, a cornerstone in training neural networks efficiently.

4. **Question7**: 
   - This notebook offers implementations of functions to generate a confusion matrix using the best parameters obtained from experiments, aiding in assessing model performance comprehensively.

5. **Question10**: 
   - Here lies the implementation of making sweeps for the MNIST dataset using 'train.py'. You can execute it via the command:
     ```
     python train.py --wandb_entity myname --wandb_project myprojectname
     ```

