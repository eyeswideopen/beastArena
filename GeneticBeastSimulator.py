#    This file is part of DEAP.
#
#    DEAP is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of
#    the License, or (at your option) any later version.
#
#    DEAP is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with DEAP. If not, see <http://www.gnu.org/licenses/>.

"""
This example is from "John R. Koza. Genetic Programming: On the Programming 
of Computers by Natural Selection. MIT Press, Cambridge, MA, USA, 1992.".

The problem is called The Artificial Ant Problem. 
<http://www.cs.ucl.ac.uk/staff/w.langdon/bloat_csrp-97-29/node2.html>

The goal of this example is to show how to use DEAP and its GP framework with
with complex system of functions and object. 

Given an AntSimulator ant, this solution should get the 89 pieces of food
within 543 moves.
ant.routine = ant.if_food_ahead(ant.move_forward, prog3(ant.turn_left, 
                                                  prog2(ant.if_food_ahead(ant.move_forward, ant.turn_right), 
                                                        prog2(ant.turn_right, prog2(ant.turn_left, ant.turn_right))),
                                                  prog2(ant.if_food_ahead(ant.move_forward, ant.turn_left), ant.move_forward)))

Best solution found with DEAP:
prog3(prog3(move_forward, 
            turn_right, 
            if_food_ahead(if_food_ahead(prog3(move_forward,
                                              move_forward, 
                                              move_forward), 
                                        prog2(turn_left, 
                                              turn_right)), 
                          turn_left)), 
      if_food_ahead(turn_left, 
                    turn_left), 
      if_food_ahead(move_forward, 
                    turn_right)) 
fitness = (89,)
"""

import copy
import random, time
from functools import partial

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
from scoop import futures
import GeneticBeast
import multiprocessing

# def progn(*args):
#     for arg in args:
#         arg()
# 
# def prog2(out1, out2): 
#     return partial(progn,out1,out2)
# 
# def prog3(out1, out2, out3):     
#     return partial(progn,out1,out2,out3)  

def if_then_else(condition, out1, out2):
    out1() if condition else out2()

game = None


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
        self.currentBeast.returnValue = self.translateToBigEnv(pos)
        return

    # own helper methods
    def translateToBigEnv(self, pos):
        return pos + 7 + pos/3*2

    def translateToSmallEnv(self, pos):
        return pos - 5 - pos/5*2

    def checkBiggerMonsterAtPos(self, pos):

        if not self.environment: return False

        return True if self.environment[self.translateToBigEnv(pos)] == ">" else False

    def checkSmallerMonsterAtPos(self, pos):

        if not self.environment: return False

        return True if self.environment[self.translateToBigEnv(pos)] == "<" else False

    def checkFoodAtPos(self, pos):
        if not self.environment: return False

        return True if self.environment[self.translateToBigEnv(pos)] == "*" else False







    def smallerBeastAt0(self, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(0), out1, out2)
    def smallerBeastAt1(self, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(1), out1, out2)
    def smallerBeastAt2(self, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(2), out1, out2)
    def smallerBeastAt3(self, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(3), out1, out2)
    def smallerBeastAt5(self, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(5), out1, out2)
    def smallerBeastAt6(self, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(6), out1, out2)
    def smallerBeastAt7(self, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(7), out1, out2)
    def smallerBeastAt8(self, out1, out2):
        return partial(if_then_else, self.checkSmallerMonsterAtPos(8), out1, out2)

    def biggerBeastAt0(self, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(0), out1, out2)
    def biggerBeastAt1(self, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(1), out1, out2)
    def biggerBeastAt2(self, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(2), out1, out2)
    def biggerBeastAt3(self, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(3), out1, out2)
    def biggerBeastAt5(self, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(5), out1, out2)
    def biggerBeastAt6(self, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(6), out1, out2)
    def biggerBeastAt7(self, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(7), out1, out2)
    def biggerBeastAt8(self, out1, out2):
        return partial(if_then_else, self.checkBiggerMonsterAtPos(8), out1, out2)


    def foodAt0(self, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(0), out1, out2)
    def foodAt1(self, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(1), out1, out2)
    def foodAt2(self, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(2), out1, out2)
    def foodAt3(self, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(3), out1, out2)
    def foodAt5(self, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(5), out1, out2)
    def foodAt6(self, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(6), out1, out2)
    def foodAt7(self, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(7), out1, out2)
    def foodAt8(self, out1, out2):
        return partial(if_then_else, self.checkFoodAtPos(8), out1, out2)

    def moveTo0(self):
        self.move(0)
    def moveTo1(self):
        self.move(1)
    def moveTo2(self):
        self.move(2)
    def moveTo3(self):
        self.move(3)
    def moveTo5(self):
        self.move(5)
    def moveTo6(self):
        self.move(6)
    def moveTo7(self):
        self.move(7)
    def moveTo8(self):
        self.move(8)




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
   
    def run(self, routine):

        self._reset()
        #add beast to beastList
        beast = GeneticBeast.GeneticBeast(self, routine)
        print("created")
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

ant = GeneticBeastRepresentation()

pset = gp.PrimitiveSet("MAIN", 0)

pset.addPrimitive(ant.smallerBeastAt0, 2)
pset.addPrimitive(ant.smallerBeastAt1, 2)
pset.addPrimitive(ant.smallerBeastAt2, 2)
pset.addPrimitive(ant.smallerBeastAt3, 2)
pset.addPrimitive(ant.smallerBeastAt5, 2)
pset.addPrimitive(ant.smallerBeastAt6, 2)
pset.addPrimitive(ant.smallerBeastAt7, 2)
pset.addPrimitive(ant.smallerBeastAt8, 2)

pset.addPrimitive(ant.biggerBeastAt0, 2)
pset.addPrimitive(ant.biggerBeastAt1, 2)
pset.addPrimitive(ant.biggerBeastAt2, 2)
pset.addPrimitive(ant.biggerBeastAt3, 2)
pset.addPrimitive(ant.biggerBeastAt5, 2)
pset.addPrimitive(ant.biggerBeastAt6, 2)
pset.addPrimitive(ant.biggerBeastAt7, 2)
pset.addPrimitive(ant.biggerBeastAt8, 2)

pset.addPrimitive(ant.foodAt0, 2)
pset.addPrimitive(ant.foodAt1, 2)
pset.addPrimitive(ant.foodAt2, 2)
pset.addPrimitive(ant.foodAt3, 2)
pset.addPrimitive(ant.foodAt5, 2)
pset.addPrimitive(ant.foodAt6, 2)
pset.addPrimitive(ant.foodAt7, 2)
pset.addPrimitive(ant.foodAt8, 2)

pset.addTerminal(ant.moveTo0)
pset.addTerminal(ant.moveTo1)
pset.addTerminal(ant.moveTo2)
pset.addTerminal(ant.moveTo3)
pset.addTerminal(ant.moveTo5)
pset.addTerminal(ant.moveTo6)
pset.addTerminal(ant.moveTo7)
pset.addTerminal(ant.moveTo8)


# pset.addPrimitive(ant.if_food_ahead, 2)
# pset.addPrimitive(prog2, 2)
# pset.addPrimitive(prog3, 3)
# pset.addTerminal(ant.move_forward)
# pset.addTerminal(ant.turn_left)
# pset.addTerminal(ant.turn_right)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("map", futures.map)
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=2)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalArtificialAnt(individual):
    # Transform the tree expression to functionnal Python code
    print("enes")
    routine = gp.evaluate(individual, pset)
    # Run the generated routine
    ant.run(routine)
    print("ant.finalEnergy: " + str(ant.finalEnergy) + " ant.currentBeast.energy: " + str(ant.currentBeast.energy))
    return ant.currentBeast.energy,

toolbox.register("evaluate", evalArtificialAnt)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut)

def main():
    print("main")

    random.seed(69)

    trail_file = open("santafe_trail.txt")
    ant.parse_matrix(trail_file)
    
    pop = toolbox.population(n=multiprocessing.cpu_count())
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", tools.mean)
    stats.register("std", tools.std)
    stats.register("min", min)
    stats.register("max", max)
    
    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 40, stats, halloffame=hof)

    file = open("dont_hassle_the_hof", "w")
    file.write(hof)
    file.close()
    
    return pop, hof, stats

if __name__ == "__main__":
    main()