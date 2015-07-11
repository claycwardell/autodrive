import pdb
import random
from time import sleep
from car import Car
import consts

total_cars = []

def all_positions():
    for i in xrange(consts.BOARD_HEIGHT):
        for j in xrange(consts.BOARD_WIDTH):
            yield (j,i)

def print_board():
    board_string = ""
    for pos in all_positions():
        cars_at_pos = get_cars_at_position(pos)
        if len(cars_at_pos) == 0:
            board_string += "-"
        elif len(cars_at_pos) == 1:
            board_string += cars_at_pos[0].draw_as
        else:
            board_string += "X"
        if pos[0] == consts.BOARD_WIDTH-1:
            board_string += "\n"
    print board_string


def get_cars_at_position(pos):
    ret = []
    for c in total_cars:
        if c.position == pos:
            ret.append(c)
    return ret


def apply_moves_safely():
    for c in total_cars:
        c.apply_move()

    wreck_positions = [pos for pos in all_positions() if len(get_cars_at_position(pos)) > 1]

    if wreck_positions:
        for w in wreck_positions:
            cars_involved = get_cars_at_position(w)

        for c in total_cars:
            c.revert_move()

        # If there is a wreck involving a car that is already stationary, the only way to
        # avoid it is to have all cars involved not move
        if consts.MOVE_NULL in [c.next_move for c in cars_involved]:
            for c in cars_involved:
                c.next_move = consts.MOVE_NULL

        # Otherwise, exactly one car should be allowed to pass
        else:
            car_to_pass = random.choice(cars_involved)
            for c in cars_involved:
                if c != car_to_pass:
                    c.next_move = consts.MOVE_NULL

        apply_moves_safely()


def apply_moves_unsafely():
    clear_crashes()
    for c in total_cars:
        c.apply_move()

def clear_crashes():
    for pos in all_positions():
        cars_at_pos = get_cars_at_position(pos)
        if len(cars_at_pos) > 1:
            for c in cars_at_pos:
                total_cars.remove(c)



def simulation_step():
    for c in total_cars:
        c.next_move = c.intended_next_move
    if consts.AVOID_CRASHES:
        apply_moves_safely()
    else:
        apply_moves_unsafely()

    for i in xrange(consts.BOARD_HEIGHT):
        pos = (0,i)
        attempt_spawn(pos, intended_next_move=consts.MOVE_RIGHT, draw_as='R')

    for i in xrange(consts.BOARD_WIDTH):
        pos = (i,0)
        attempt_spawn(pos, intended_next_move=consts.MOVE_DOWN, draw_as='D')
    clean_cars()
    print_board()


def clean_cars():
    """
    Gets rid of cars that have completed their journey
    """
    for c in total_cars:
        if c.x >= consts.BOARD_WIDTH:
            total_cars.remove(c)
        elif c.y >= consts.BOARD_HEIGHT:
            total_cars.remove(c)


def attempt_spawn(pos, intended_next_move, draw_as):
    if not get_cars_at_position(pos) and random.random() < consts.SPAWN_FREQUENCY:
        car = Car(position=pos, intended_next_move=intended_next_move, draw_as=draw_as)
        car.intended_next_move = intended_next_move
        total_cars.append(car)







