import random
import consts

class CarInitException(ValueError):
    pass

class Car(object):
    """
    Represents a self driving car.  Cars start at the edge of the board and want to progress in a straight line to the
    far side.  The only edge case is if they start in the top left corner -- then they could reasonably progress
    either across or down.  If so, their destination is selected randomly from those two options.
    """

    def __init__(self, position, intended_next_move, draw_as):
        self.position = position
        self.intended_next_move = intended_next_move
        self.next_move = consts.MOVE_NULL
        self.draw_as = draw_as

        starts_left = self.x == 0
        starts_top = self.y == 0

        if starts_left and starts_top:
            self.destination = random.choice([(consts.BOARD_WIDTH-1, 0), (0, consts.BOARD_HEIGHT-1)])
        elif starts_left:
            self.destination = (consts.BOARD_WIDTH-1, self.y)
        elif starts_top:
            self.destination = (self.x, consts.BOARD_HEIGHT-1)
        else:
            raise CarInitException("Car must start at edge of board")


    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    @property
    def x_move(self):
        return self.next_move[0]

    @property
    def y_move(self):
        return self.next_move[1]

    def apply_move(self):
        self.position = (self.x + self.x_move, self.y + self.y_move)

    def revert_move(self):
        self.position = (self.x - self.x_move, self.y - self.y_move)


    def __str__(self):
        return self.draw_as