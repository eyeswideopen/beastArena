from functools import partial

import copy
import GeneticBeast


def progn(*args):
    for arg in args:
        arg()


def prog2(out1, out2):
    return partial(progn, out1, out2)


def prog3(out1, out2, out3):
    return partial(progn, out1, out2, out3)


def if_then_else(condition, out1, out2):
    out1() if condition() else out2()


class GeneticBeastRepresentation():
    def __init__(self):

        self.simulator = None
        self.currentBeast = None
        self.environment = None
        self.finalEnergy = 0

    def _reset(self):
        self.currentBeast = None
        self.finalEnergy = None
        self.environment = None


    # own primitives
    def ifFoodAtPosition(self, pos, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(pos), out1, out2)

    def ifBiggerMonsterAtPosition(self, pos, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(pos), out1, out2)

    def ifSmallerMonsterAtPosition(self, pos, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(pos), out1, out2)

    # own terminal
    def move(self, pos):
        self.currentBeast.returnValue = pos
        return

    # own helper methods
    def translateToBigEnv(self, pos):
        return pos + 7 + pos/3*2

    def translateToSmallEnv(self, pos):
        return pos - 5 - pos/5*2

    def checkBiggerMonsterAtPos(self, pos):
        return True if self.environment[self.translateToBigEnv(pos)] == ">" else False

    def checkSmallerMonsterAtPos(self, pos):
        return True if self.environment[self.translateToBigEnv(pos)] == "<" else False

    def checkFoodMonsterAtPos(self, pos):
        return True if self.environment[self.translateToBigEnv(pos)] == "*" else False


    @property
    def position(self):
        return (self.row, self.col, self.direction[self.dir])

    def turn_left(self):

        if self.moves < self.max_moves:
            self.moves += 1
            self.dir = (self.dir - 1) % 4

    def turn_right(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.dir = (self.dir + 1) % 4

    def move_forward(self):
        if self.moves < self.max_moves:
            self.moves += 1
            self.row = (self.row + self.dir_row[self.dir]) % self.matrix_row
            self.col = (self.col + self.dir_col[self.dir]) % self.matrix_col
            if self.matrix_exc[self.row][self.col] == "food":
                self.eaten += 1
            self.matrix_exc[self.row][self.col] = "passed"

    def sense_food(self):
        ahead_row = (self.row + self.dir_row[self.dir]) % self.matrix_row
        ahead_col = (self.col + self.dir_col[self.dir]) % self.matrix_col
        return self.matrix_exc[ahead_row][ahead_col] == "food"

    def if_food_ahead(self, out1, out2):
        return partial(if_then_else, self.sense_food, out1, out2)


    def doRound(self, routine):
        self._reset()
        #add beast to beastList
        beast = GeneticBeast.GeneticBeast(self, routine)
        print("created")
        self.simulator.addBeast(beast)
        beast.play()

    def parse_matrix(self, matrix):
        self.matrix = list()
        for i, line in enumerate(matrix):
            self.matrix.append(list())
            for j, col in enumerate(line):
                if col == "#":
                    self.matrix[-1].append("food")
                elif col == ".":
                    self.matrix[-1].append("empty")
                elif col == "S":
                    self.matrix[-1].append("empty")
                    self.row_start = self.row = i
                    self.col_start = self.col = j
                    self.dir = 1
        self.matrix_row = len(self.matrix)
        self.matrix_col = len(self.matrix[0])
        self.matrix_exc = copy.deepcopy(self.matrix)
