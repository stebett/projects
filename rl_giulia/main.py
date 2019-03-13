from grid import Grid
from agent import Agent

dimension = 4 
discount = 0.9
target = [4, 4]
train_iterations = 200
demo_iterations = 7


grid = Grid(dimension)
agent = Agent(dimension, target, discount)

def turn(where, who):
    who.get_real_pos(where.current_state)
    is_over = who.evaluate_q_value()
    if is_over == 'finish':
        grid.spawn()
        return 'Won!'
    else:
        move = (who.choose_move())
        where.move(who.choose_move())

def train(train_iter, where, who):
    count = 0
    for i in range(train_iter):
        if turn(where, who) == 'Won!':
            count +=1
    print("You won {} times on {} iterations!".format(count, train_iter))
    return who.q_values


def demostrate(demo_iter, where, who):
    grid.spawn()
    for i in range(demo_iter):
        print('\n', where.draw())
        turn(where, who)


print(train(train_iterations, grid, agent))
demostrate(demo_iterations, grid, agent)
