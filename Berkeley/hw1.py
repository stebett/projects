import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pickle as pkl
import pandas as pd
import gym
import numpy as np

# Global Variables

max_iter = 300
environ = 'Reacher-v2'
render = True


# Load Data
with open('expert_data/{}.pkl'.format(environ), 'rb') as f:
    data = pkl.load(f)

exp_obs = data['observations']
exp_act = data['actions']
exp_act = exp_act.reshape([exp_act.shape[0], exp_act.shape[2]])

model = keras.Sequential([
    layers.Dense(exp_obs.shape[1], activation=tf.nn.relu),
    layers.Dense(exp_obs.shape[1], activation=tf.nn.relu),
    layers.Dense(exp_act.shape[1])])

# Train Model
model.compile(
        loss='mean_squared_error',
        optimizer=tf.keras.optimizers.RMSprop(0.001),
        metrics=['mean_absolute_error', 'mean_squared_error'])

model.fit(exp_obs, exp_act)

# Initialize Environment
env = gym.make(environ)

for i in range(max_iter):

    obs = env.reset()

    for x in range(30):
        if render:
            env.render()
        action = model.predict(obs.reshape(1,len(obs)))
        obs, r, done, _ = env.step(action)

        

    
    

    

