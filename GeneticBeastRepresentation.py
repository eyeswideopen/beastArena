import GeneticBeast

class GeneticBeastRepresentation():
    direction = ["north","east","south","west"]
    dir_row = [1, 0, -1, 0]
    dir_col = [0, 1, 0, -1]


    def __init__(self, max_moves):

        self.max_moves = max_moves
        self.moves = 0
        self.eaten = 0
        self.routine = None
        self.row_start =0
        self.col_start=0

        self.moving = False
        self.returning = None
        self.environment = ""

        
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
        beast = GeneticBeast(self,routine)
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
