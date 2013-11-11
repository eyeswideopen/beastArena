import copy
import random,threading

import numpy

from functools import partial

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from scoop import futures



def progn(*args):
    for arg in args:
        arg()

def prog2(out1, out2): 
    return partial(progn,out1,out2)

def prog3(out1, out2, out3):     
    return partial(progn,out1,out2,out3)  

def if_then_else(condition, out1, out2):
    out1() if condition() else out2()


class GeneticBeastFactory(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.ant = GeneticBeast(600)

        self.pset = gp.PrimitiveSet("MAIN", 0)
        self.pset.addPrimitive(self.ant.if_food_ahead, 2)
        self.pset.addPrimitive(prog2, 2)
        self.pset.addPrimitive(prog3, 3)
        self.pset.addTerminal(self.ant.move_forward)
        self.pset.addTerminal(self.ant.turn_left)
        self.pset.addTerminal(self.ant.turn_right)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)
        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("expr_init", gp.genFull, pset=self.pset, min_=1, max_=2)

        # Structure initializers
        self.toolbox.register("map",futures.map)
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.expr_init)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)



        self.toolbox.register("evaluate", self.evalArtificialAnt)
        self.toolbox.register("select", tools.selTournament, tournsize=7)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", gp.mutUniform, expr=self.toolbox.expr_mut, pset=self.pset)
        self.start()


    def evalArtificialAnt(self,individual):
        # Transform the tree expression to functionnal Python code
        routine = gp.evaluate(individual, self.pset)
        # Run the generated routine
        self.ant.doRound(routine)

        return self.ant.eaten,

    def run(self):

        random.seed(69)
        trail_file = open("santafe_trail.txt")
        self.ant.parse_matrix(trail_file)
        pop = self.toolbox.population(n=300)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        algorithms.eaSimple(pop, self.toolbox, 0.5, 0.2, 40, stats, halloffame=hof)

counter=0


class GeneticBeast(threading.Thread):
    direction = ["north","east","south","west"]
    dir_row = [1, 0, -1, 0]
    dir_col = [0, 1, 0, -1]


    def bewege (self, environment):

        self.environment = environment
        self.move.acquire()
        self.moving = True
        self.returnReady.acquire()
        self.move.notify()
        self.move.release()
        if not self.returning:
            self.returnReady.wait()
        ret = self.returning
        self.returning = None
        self.returnReady.release()

        return ret
    
    def __init__(self, max_moves):
        threading.Thread.__init__(self)

        self.max_moves = max_moves
        self.moves = 0
        self.eaten = 0
        self.routine = None
        self.row_start =0
        self.col_start=0

        self.moving = False
        self.returning = None
        self.environment = ""
        self.move = threading.Condition()
        self.returnReady = threading.Condition()
        self.start()

        
    def _reset(self):
        self.row = self.row_start 
        self.col = self.col_start 
        self.dir = 1
        self.moves = 0  
        self.eaten = 0
        self.matrix_exc = copy.deepcopy(self.matrix)
        self.moving = False
        self.returning = False

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



    def run(self):
        counter = 0
        while not "Ende" in self.environment:
            self.move.acquire()
            if not self.moving:
                self.move.wait()
            self.returnReady.acquire()
            self.moving = False

            ## do move shit here!

            self.routine()
            ##return value here!
            self.returning = counter

            self.move.release()
            self.returnReady.notify()
            self.returnReady.release()


    def doRound(self,routine):
        self._reset()
        self.routine = routine

        while self.moves < self.max_moves:
            self.bewege("")

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



if __name__=="__main__":
    f=GeneticBeastFactory()




