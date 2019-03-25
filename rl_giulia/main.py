import numpy as np
from grid import Grid
from agent import Agent
dimension = 4
discount = 0.9
target = [4, 4]

grid = Grid(dimension)
agent = Agent(dimension, target, discount)


def turn(where, who):
    who.get_real_pos(where.current_state)
    is_over = who.evaluate_q_value()
    if is_over == 'finish':
        grid.spawn()
        return 'Won!'
    elif is_over == 'converged':
        return 'Converged!'
    else:
        next_move = who.choose_move()
        where.move(next_move)
        return next_move


def train(where, who):
    count = 0
    converged = False
    old_q_values = np.sum(who.q_values)
    while not converged:
        count += 1
        output = turn(where, who)
        if output == 'Won!':
            new_q_values = np.sum(who.q_values)
            if abs(old_q_values - new_q_values) == 0:
                if count > 2000:
                    converged = 1
            old_q_values = np.sum(who.q_values)
    print("You converged in {} iterations!".format(count))
    return who.q_values


def demonstrate(where, who):
    grid.spawn()
    has_won = -1
    while has_won:
        where.draw()
        who.get_real_pos(where.current_state)
        has_won = who.take_reward()
        next_move = who.choose_move()
        where.move(next_move)
        if has_won == -1:
            print(next_move)
        else:
            print('You Won!!')


q_values_end = train(grid, agent)
print(q_values_end)
demonstrate(grid, agent)
