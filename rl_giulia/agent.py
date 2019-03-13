from grid import Grid
import random as rd
import numpy as np

# Questo agente e' basato su un algoritmo con diverse caratteristiche:
# 1) q_learning -> Non attribuisce valori agli stati ma alle azioni
# 2) TD(0) -> Temporal Difference 0, ovvero ogni mossa rielabora i valori delle
# azioni
# 3) off-policy -> Agisce sempre nel modo piu' conveniente (greedy)
class Agent:
    def __init__(self, grid_shape, target, discount):
        self.max_lenght = grid_shape - 1
        self.q_values = np.zeros([grid_shape, grid_shape])
        self.target = (target[0] - 1, target[1] - 1)
        self.gamma = discount
        self.pos = None

    def get_real_pos(self, position):
        real_position = (position[0] - 1, position[1] - 1) # Altrimenti numpy sclera
        self.pos = real_position

    def look_around(self):
        # Legge i valori attesi di ogni mossa possibile
        top_val= ((self.pos[0] - 1, self.pos[1])
                   if self.pos[0] - 1 >= 0
                   else (self.pos[0], self.pos[1]))
        bot_val = ((self.pos[0] + 1, self.pos[1])
                   if self.pos[0] + 1 <= self.max_lenght
                   else (self.pos[0], self.pos[1]))
        left_val = ((self.pos[0], self.pos[1] - 1)
                    if self.pos[1] - 1 >= 0
                    else (self.pos[0], self.pos[1]))
        right_val = ((self.pos[0], self.pos[1] + 1)
                     if self.pos[1] + 1 <= self.max_lenght
                     else (self.pos[0], self.pos[1]))

        neighbours = ((bot_val, 'bot'),
                      (top_val, 'top'),
                      (left_val, 'left'),
                      (right_val, 'right'))
        move_dict = {neighbours[pos][1]: self.q_values[neighbours[pos][0]] for pos in range(4)}

        return move_dict


    def choose_move(self):
        move_values = self.look_around()

        max_value = max(move_values.values())

        top_moves = []
        chosen_move = None
        for key, value in move_values.items():
            if value == max_value:
                top_moves.append(key)

        if len(top_moves) > 1:
            chosen_move = top_moves[rd.randint(0, len(top_moves) - 1)]
        else:
            chosen_move = top_moves[0]

        return chosen_move


    def take_reward(self):
        if self.pos == self.target:
            return 0
        else:
            return -1

    def evaluate_q_value(self):
        reward = self.take_reward()
        if reward == 0:
            self.q_values[self.pos] = 0
            return 'finish'
        move_values = self.look_around()
        new_q_value = 0.25*sum(move_values.values())*self.gamma + reward # Algoritmone
        self.q_values[self.pos] = new_q_value
        return 'going on'
