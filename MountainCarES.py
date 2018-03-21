import gym
import math
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation
import collections

class BlackBox:
    def __init__(self):
        self._init_model()

    def _init_model(self):
        model = Sequential([
            Dense(2, input_dim=2, activation='relu'),
            Dense(3, activation='softmax'),
            ])
        self.model = model
        self.shape = [2,3]
        return

    def flatten(self, weights):
        w = []
        for l in weights:
            if isinstance(l, collections.Iterable):
                w = w + flatten(l)
            else:
                w = w + [l]
        return w

    def unflatten(self, flat_weights, shape=[2,3]):
        w = []
        i = 0
        for l, size in enumerate(shape):
            layer = self.model.layers[l].get_weights()
            params = layer[0]
            bias = layer[1]
            new_layer = []
            new_params = []
            new_bias = []
            for param in params:
                new_params.append(flat_weights[i:i+size])
                i += size
            for b in bias:
                new_bias.append(flat_weights[i])
                i += 1
            w.append(np.array(new_params))
            w.append(np.array(new_bias))
        return w

    def get_weights(self):
        return self.model.get_weights()

    def set_weights(self, weights):
        self.model.set_weights(weights)

    def get_flat_weights(self):
        return self.flatten(self.get_weights())

    def set_flat_weights(self, flat_weights):
        return self.set_weights(self.unflatten(flat_weights))

    def produce_action(self, state):
        inp = np.array([np.array(state).T])
        return np.argmax(model.predict)


env = gym.make('MountainCar-v0')
alpha = 0.1
sigma = 3
bb = BlackBox()
w = bb.get_flat_weights()
pop_size = 200

def run_sim():
    for i_episode in range(20):
        observation = env.reset()
        for t in range(200):
            env.render()
            action = 2#env.action_space.sample()
            if math.ceil(math.sqrt(t)) % 2:
                action = 2
                print("action = ", 2)
            else:
                action = 0
                print("action = ", 0)
            observation, reward, done, info = env.step(action)
            #  print(observation)
            if done:
                print("Episode finished after {} timesteps".format(t+1))
                exit()
                break

"""
We need a distribution over parameters p_psi(theta) parameterized by psi.

Maximize the average objective value E_(theta sampled from p_psi)F(theta)
over the population by searching for psi with stochastic gradient ascent.
Using the score function estimator for Delta_psi E_(theta sampled from p_psi)F(theta)

When p_psi is a factored gaussian, the resulting gradient estimator is also know as:
    simultaneous perturbation stochastic approximation
    parameter exploring gradients
    zero-order gradient estimation
"""

        
if __name__ == '__main__':
    run_sim()

