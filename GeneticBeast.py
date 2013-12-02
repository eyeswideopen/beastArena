import time
from Client import Client


class GeneticBeast():
    def __init__(self, rep, routine):
        self.routine = routine
        self.rep = rep
        self.energy = None
        self.returnValue = 0
        self.environment = ""

        self.client = Client("127.0.0.1", "8", self)

    def bewege(self, paramString):
        print("bewege!")

        params = paramString.split(';', 2)
        if len(params[0]) > 0:
            energy = int(params[0])
        else:
            energy = 0

        environment = params[1]

        self.environment = environment
        self.rep.currentBeast = self

        self.routine()

        if energy == 0 or "Ende" in environment:
            self.energy = energy

        return self.returnValue


    def play(self):

        print("play called" + str(id(self)))
        self.client.connectToServer()
        self.client.registration()


        #waiting till game is finished
        self.client.listening()

        self.rep.finalEnergy = self.energy




