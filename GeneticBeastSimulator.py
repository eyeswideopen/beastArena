import copy
import random,threading

import numpy

from functools import partial
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
import GeneticBeastRepresentation, GeneticBeast


def progn(*args):
    for arg in args:
        arg()

def prog2(out1, out2): 
    return partial(progn,out1,out2)

def prog3(out1, out2, out3):     
    return partial(progn,out1,out2,out3)  

def if_then_else(condition, out1, out2):
    out1() if condition() else out2()


class GeneticBeastSimulator(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.beastRepresentation = GeneticBeastRepresentation(600)

        self.pset = gp.PrimitiveSet("MAIN", 0)
        self.pset.addPrimitive(self.beastRepresentation.if_food_ahead, 2)
        self.pset.addPrimitive(prog2, 2)
        self.pset.addPrimitive(prog3, 3)
        self.pset.addTerminal(self.beastRepresentation.move_forward)
        self.pset.addTerminal(self.beastRepresentation.turn_left)
        self.pset.addTerminal(self.beastRepresentation.turn_right)

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=self.pset,beast=GeneticBeastRepresentation(300))
        self.toolbox = base.Toolbox()

        # Attribute generator
        self.toolbox.register("expr_init", gp.genFull, pset=self.pset, min_=1, max_=2)

        # Structure initializers
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.expr_init)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)



        self.toolbox.register("evaluate", self.evalArtificialAnt)
        self.toolbox.register("select", tools.selTournament, tournsize=7)
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
        self.toolbox.register("mutate", gp.mutUniform, expr=self.toolbox.expr_mut)
        self.start()


    def evalArtificialAnt(self,individual):
        # Transform the tree expression to functionnal Python code
        routine = gp.evaluate(individual, self.pset)
        # Run the generated routine
        self.beastRepresentation.doRound(routine)

        return self.beastRepresentation.eaten,

    def run(self):

        random.seed(69)
        trail_file = open("santafe_trail.txt")
        self.beastRepresentation.parse_matrix(trail_file)
        pop = self.toolbox.population(n=300)
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        algorithms.eaSimple(pop, self.toolbox, 0.5, 0.2, 40, stats, halloffame=hof)




if __name__=="__main__":
    f=GeneticBeastSimulator()




