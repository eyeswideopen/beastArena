import time
from Client import Client


class GeneticBeast():
    def __init__(self, rep, routine):
        self.routine = routine
        self.rep = rep
        self.returnValue = 13
        self.environment = ""

        self.client = Client("127.0.0.1", "8", self)

    def bewege(self, paramString):
        print("bewege!")

        params = paramString.split(';', 2)
        if len(params[0]) > 0:
            energy = int(params[0])
        else:
            energy = 0

        self.environment = params[1]
        self.rep.environment = self.environment
        self.rep.currentBeast = self

        self.routine()

        if energy == 0 or "Ende" in self.environment:
            self.rep.finalEnergy = energy

        return self.returnValue


    def play(self):

        print("play called" + str(id(self)))
        self.client.connectToServer()
        self.client.registration()


        #waiting till game is finished
        self.client.listening()






