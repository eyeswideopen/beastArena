import time
class GeneticBeast():

    def __init__(self, rep, routine):
        self.routine = routine
        self.rep = rep
        self.energy = None
        self.returnValue=0
        self.environment=""

    def bewege (self, paramString):

        params = paramString.split(';', 2)
        if len(params[0]) > 0:
            energy = int(params[0])
        else:
            energy = 0

        environment = params[1]

        self.environment=environment
        self.rep.currentBeast=self

        self.routine()

        if energy==0 or "Ende" in environment:
            self.energy=energy


        return self.returnValue


    def play(self):
        while not self.energy:
            time.sleep(0.1)

        self.rep.finalEnergy=self.energy