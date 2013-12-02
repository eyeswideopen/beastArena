import random
import threading
import numpy
from functools import partial
from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp
import time, multiprocessing
from scoop import futures
from GeneticBeastRepresentation import GeneticBeastRepresentation
from BeastArena import beast_arena

def progn(*args):
    for arg in args:
        arg()


def prog2(out1, out2):
    return partial(progn, out1, out2)


def prog3(out1, out2, out3):
    return partial(progn, out1, out2, out3)

beastRepresentation=GeneticBeastRepresentation(600)

pset = gp.PrimitiveSet("MAIN", 0)
pset.addPrimitive(beastRepresentation.if_food_ahead, 2)
pset.addPrimitive(prog2, 2)
pset.addPrimitive(prog3, 3)
pset.addTerminal(beastRepresentation.move_forward)
pset.addTerminal(beastRepresentation.turn_left)
pset.addTerminal(beastRepresentation.turn_right)


def evalArtificialAnt(individual):
    # Transform the tree expression to functionnal Python code
    routine = gp.evaluate(individual, pset)
    # Run the generated routine
    beastRepresentation.doRound(routine)
    print(id(individual))

    return beastRepresentation.eaten,


creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax, pset=pset)
toolbox = base.Toolbox()

toolbox.register("map", futures.map)

# Attribute generator
toolbox.register("expr_init", gp.genFull, pset=pset, min_=1, max_=2)

# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr_init)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evalArtificialAnt)
toolbox.register("select", tools.selTournament, tournsize=7)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genFull, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut)



class GeneticBeastSimulator(threading.Thread):
    def __init__(self, game):
        threading.Thread.__init__(self)
        global beastRepresentation
        beastRepresentation.setSimulator(self)

        self.game = game
        self.beastList = []


    def addBeast(self, beast):
        self.beastList.append(beast)
        if len(self.beastList) == multiprocessing.cpu_count():
            self.game.geneticBeasts = self.beastList


    def run(self):
        pass


if __name__ == "__main__":
    game = beast_arena()
    game.start()
    GeneticBeastSimulator(game)
    random.seed(69)
    trail_file = open("santafe_trail.txt")
    beastRepresentation.parse_matrix(trail_file)
    pop = toolbox.population(n=300)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 40, stats, halloffame=hof)




