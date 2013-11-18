class GeneticBeast():

    def __init__(self, rep, routine):
        self.routine = routine
        self.rep = rep
        self.energy = None

    def bewege (self, environment):

        self.rep.environment = environment

        self.routine()

        return self.rep.returnValue

    def play(self):

        while not self.energy:
            continue