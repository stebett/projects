import random as rd
from pandas import DataFrame as df


class Grid():
    def __init__(self, dimension):
        self.dim = [dimension, dimension]  # Starts from 1
        self.current_state = []

        self.spawn()

    def draw(self):
        grid_full = []
        for y in range(1, self.dim[1] + 1):
            grid_row = []
            grid_full.append(grid_row)
            for x in range(1, self.dim[1] + 1):
                if [y, x] == self.current_state:
                    grid_row.append('X')
                else:
                    grid_row.append('#')
        return df(grid_full)

    def spawn(self):
        new_x = rd.randint(1, self.dim[1])
        new_y = rd.randint(1, self.dim[0])
        self.current_state = [new_y, new_x]

    def move(self, direction):  # This function is obrobrious
        old_state = self.current_state
        if direction not in ['right', 'left', 'top', 'bot']:
            return 'Invalid direction'

        elif direction == 'right':
            new_x = old_state[1] + 1
            if new_x > self.dim[1]:
                self.current_state = old_state  # Useless but clear
            else:
                self.current_state = [old_state[0], new_x]

        elif direction == 'left':
            new_x = old_state[1] - 1
            if new_x <= 0:
                self.current_state = old_state  # Useless but clear
            else:
                self.current_state = [old_state[0], new_x]

        elif direction == 'top':
            new_y = old_state[0] - 1
            if new_y <= 0:
                self.current_state = old_state  # Useless but clear
            else:
                self.current_state = [new_y, old_state[1]]

        elif direction == 'bot':
            new_y = old_state[0] + 1
            if (new_y > self.dim[1]):
                self.current_state = old_state  # Useless but clear
            else:
                self.current_state = [new_y, old_state[1]]
