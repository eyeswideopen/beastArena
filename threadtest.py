import threading


class Server:
    def __init__(self):
        self.beasts = [Client(), Client()]

    def run(self):
        while True:
            for c in self.beasts:
                print(c.bewege())


class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.moving = False
        self.returning = None
        self.environment = ""
        self.move = threading.Condition()
        self.returnReady = threading.Condition()
        self.start()

    def run(self):
        counter = 0
        while not "Ende" in self.environment:

            self.move.acquire()
            if not self.moving:
                self.move.wait()
            self.returnReady.acquire()
            self.moving = False

            ## do move shit here!
            counter += 1
            ##return value here!
            self.returning = counter

            self.move.release()
            self.returnReady.notify()
            self.returnReady.release()>

    def bewege(self):
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


if __name__ == "__main__":
    s = Server()
    s.run()