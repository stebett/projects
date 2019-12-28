import random as rd

# Questo file definisce la classe Grid,
# che e' semplicemente l'ambiente dove
# l'agente si muove.
# Le uniche cose che fa sono:
# printare la posizione,
# creare la griglia con una posizione casuale e
# muovere l'agente all'interno


class Grid():
    def __init__(self, dimension):
        # Inizializzo la griglia con dimensioni che
        # partono da 1, non so bene perche'
        self.dim = [dimension, dimension]
        self.current_state = []

        self.spawn()

    def draw(self):
        # Printa una lista di liste come mi hai insegnato tu
        grid_full = []
        for y in range(1, self.dim[1] + 1):
            grid_row = []
            grid_full.append(grid_row)
            for x in range(1, self.dim[1] + 1):
                if [y, x] == self.current_state:
                    grid_row.append('X')
                else:
                    grid_row.append('#')
        for item in grid_full:
            print(item)

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
