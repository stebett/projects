import numpy as np


class Agent(k=10, epsilon=0.2):
    def __init__(self):
        self.est_q = np.zeros(10)


def argmax_tiebreaking(arr):
    top = np.max(arr)
    ties = []
    for n, i in enumerate(arr):
        (ties.append(n) if i == top else None)

    return np.random.choice(ties)


def select_action():
    if np.random.random() < epsilon:
        action = np.random.choice(10)
    else:
        action = argmax_tiebreaking(est_q)

    return action


def update_values(est_q

# Environment
real_q=np.random.normal(0, 1, k)

def reward_generator(act):
    real_action_value = real_q[action]
    return np.random.normal(real_action_value, 1, 1)
