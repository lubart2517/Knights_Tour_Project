# Write your code here
import numpy as np
import copy
import pickle


class KnightGame:
    def __init__(self):
        self.x_size = 0
        self.y_size = 0
        self.x_pos = 0
        self.y_pos = 0
        self.field = []
        self.visited = 1
        self.first = True  # flag to compute is it the first turn or not for process function
        self.solution = []

    def print_field(self):
        available_moves = self.get_available_moves(self.x_pos, self.y_pos)
        pr_field = copy.deepcopy(self.field)
        pr_field[self.y_pos - 1][self.x_pos - 1] = 1  # set start point on the field
        if available_moves:
            for j in available_moves:
                if pr_field[j[1] - 1][j[0] - 1] != 3:
                    pr_field[j[1] - 1][j[0] - 1] = 2 # set points of available moves
        underscore = '_' * len(str(round(self.x_size * self.y_size)))

        print("-" * (self.x_size * (len(underscore) + 1) + 3))  # print top border

        for y in range(1, self.y_size + 1): # make list with text values of current row for next printing
            row = pr_field[self.y_size - y]
            lst = []
            for k in range(0, len(row)):
                if row[k] == 0:
                    lst.append(underscore)
                if row[k] == 1:
                    lst.append((len(underscore) - 1) * ' ' + 'X')
                if row[k] == 3:
                    lst.append((len(underscore) - 1) * ' ' + '*')
                if row[k] == 2:
                    next_moves = len(self.get_available_moves(k + 1, self.y_size - y + 1)) - 1
                    lst.append((len(underscore) - 1) * ' ' + str(next_moves))
            print(f"{self.y_size +1 - y}| {' '.join(lst)} |")
        print("-" * (self.x_size * (len(underscore) + 1) + 3))  # print bottom border
        print('   ' + ' ' * (len(underscore) - 1) +  # print column indexes
              (' ' * len(underscore)).join([str(x) for x in range(1, self.x_size+1)]))

    def get_available_moves(self, x_pos, y_pos):
        # return list with x and y positions of available moves for received start position
        operations = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
        available = []
        for x in operations:
            if 0 < (x_pos + x[0]) <= self.x_size and 0 < (y_pos + x[1]) <= self.y_size:  # check if point in field
                if self.field[y_pos + x[1] - 1][x_pos + x[0] - 1] != 3:  # check if point is visited
                    available.append([x_pos + x[0], y_pos + x[1]])
        return available

    def process_board_size(self):
        # function process user's input and save in self class properties board x_size and y_size
        while True:
            size = input('Enter your board dimensions: >')
            sizes = size.split()
            if len(sizes) != 2:
                print('Invalid dimensions!')
            else:
                try:
                    x_size = int(sizes[0])
                    y_size = int(sizes[1])
                    if x_size <= 0 or y_size <= 0:
                        print('Invalid dimensions!')
                    else:
                        self.x_size = x_size
                        self.y_size = y_size
                        self.field = np.zeros((y_size, x_size))
                        break
                except ValueError:
                    print('Invalid dimensions!')

    def process_input(self):
        # get user input with coordinates of next turn and save in self properties if they correct
        while True:
            if self.first:
                ask = "Enter the knight's starting position: >"
                error_message = 'Invalid position!'
            else:
                ask = "Enter your next move: >"
                error_message = 'Invalid move!'
            inp = input(ask)
            positions = inp.split()
            if len(positions) != 2:
                print(error_message)
            else:
                try:
                    x_pos = int(positions[0])
                    y_pos = int(positions[1])
                    if x_pos < 1 or x_pos > self.x_size or y_pos < 1 or y_pos > self.y_size:
                        print(error_message)
                    else:
                        if self.first:
                            choice = input('Do you want to try the puzzle? (y/n): >')
                            result = self.find_solution(np.zeros((self.y_size, self.x_size)),
                                                        x_pos, y_pos, self.x_size, self.y_size, [])
                            if result == 0:
                                print('No solution exists!')
                                exit()
                            else:
                                if choice.lower() == 'n':
                                    print("Here's the solution!")
                                    self.print_solution()
                                    exit()
                                else:
                                    self.x_pos = x_pos
                                    self.y_pos = y_pos
                                    self.print_field()
                                    self.first = False
                        else:
                            if self.validate_turn(x_pos, y_pos):
                                self.make_turn(x_pos, y_pos)
                                break
                            else:
                                print(error_message)
                except ValueError:
                    print(error_message)

    def print_solution(self):
        solution = self.solution[:int(self.x_size * self.y_size)+1]
        print_field = np.zeros((self.y_size, self.x_size))
        for k in range(0, len(solution)):
            print_field[solution[k][1] - 1][solution[k][0] - 1] = k + 1
        underscore = '_' * len(str(round(self.x_size * self.y_size)))
        print("-" * (self.x_size * (len(underscore) + 1) + 3))  # print top border

        for y in range(1, self.y_size + 1):  # make list with text values of current row for next printing
            row = print_field[self.y_size - y]
            lst = []
            for k in range(0, len(row)):
                lst.append((len(underscore) - len(str(int(row[k])))) * ' ' + str(int(row[k])))
            print(f"{self.y_size + 1 - y}| {' '.join(lst)} |")
        print("-" * (self.x_size * (len(underscore) + 1) + 3))  # print bottom border
        print('   ' + ' ' * (len(underscore) - 1) +  # print column indexes
              (' ' * len(underscore)).join([str(x) for x in range(1, self.x_size + 1)]))

    def make_turn(self, x_pos, y_pos):
        self.field[self.y_pos - 1][self.x_pos - 1] = 3  # set point as visited
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.visited += 1
        self.print_field()

    def check_end_game(self):
        if self.visited == self.x_size * self.y_size:
            print('What a great tour! Congratulations!')
            return True
        else:
            if len(self.get_available_moves(self.x_pos, self.y_pos)) == 0:
                print("No more possible moves!")
                print(f"Your knight visited {self.visited} squares!")
                return True
            else:
                return False

    def validate_turn(self, x_pos, y_pos):  # check if user turn in possible moves
        possible_moves = self.get_available_moves(self.x_pos, self.y_pos)
        if [x_pos, y_pos] in possible_moves and self.field[self.y_pos - 1][self.x_pos - 1] != 3:
            return True
        else:
            return False

    def main_loop(self):
        self.process_board_size()
        while True:
            end = self.check_end_game()
            if end:
                break
            else:
                self.process_input()

    @staticmethod
    def get_available_moves_static(field, x_pos, y_pos, x_size, y_size):
        # return list with x and y positions of available moves for received start position
        operations = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
        available = []
        for x in operations:
            if 0 < (x_pos + x[0]) <= x_size and 0 < (y_pos + x[1]) <= y_size:  # check if point in field
                if field[y_pos + x[1] - 1][x_pos + x[0] - 1] != 3:  # check if point is visited
                    available.append([x_pos + x[0], y_pos + x[1]])
        return available

    @staticmethod
    def check_end_game_static(field, x_pos, y_pos, x_size, y_size):

        if np.count_nonzero(field == 0) == 0:
            return 3
        else:
            if len(KnightGame.get_available_moves_static(field, x_pos, y_pos, x_size, y_size)) == 0:
                return 0
            else:
                return 1

    @staticmethod
    def print_field_static(field, x_pos, y_pos, x_size, y_size):
        available_moves = KnightGame.get_available_moves_static(field, x_pos, y_pos, x_size, y_size)
        pr_field = copy.deepcopy(field)
        pr_field[y_pos - 1][x_pos - 1] = 1  # set start point on the field
        if available_moves:
            for j in available_moves:
                if pr_field[j[1] - 1][j[0] - 1] != 3:
                    pr_field[j[1] - 1][j[0] - 1] = 2  # set points of available moves
        underscore = '_' * len(str(round(x_size * y_size)))

        print("-" * (x_size * (len(underscore) + 1) + 3))  # print top border

        for y in range(1, y_size + 1): # make list with text values of current row for next printing
            row = pr_field[y_size - y]
            lst = []
            for k in range(0, len(row)):
                if row[k] == 0:
                    lst.append(underscore)
                if row[k] == 1:
                    lst.append((len(underscore) - 1) * ' ' + 'X')
                if row[k] == 3:
                    lst.append((len(underscore) - 1) * ' ' + '*')
                if row[k] == 2:
                    next_moves = len(KnightGame.get_available_moves_static(field, k + 1, y_size - y + 1, x_size, y_size)) - 1
                    lst.append((len(underscore) - 1) * ' ' + str(next_moves))
            print(f"{y_size +1 - y}| {' '.join(lst)} |")
        print("-" * (x_size * (len(underscore) + 1) + 3))  # print bottom border
        print('   ' + ' ' * (len(underscore) - 1) +  # print column indexes
              (' ' * len(underscore)).join([str(x) for x in range(1, x_size+1)]))

    def find_solution(self, field, x_pos, y_pos, x_size, y_size, solutions):
        if self.solution:
            return 0
        else:
            field[y_pos - 1][x_pos - 1] = 3
            check = KnightGame.check_end_game_static(field, x_pos, y_pos, x_size, y_size)
            # KnightGame.print_field_static(field, x_pos, y_pos, x_size, y_size)
            if check == 3:
                solutions.append([x_pos, y_pos])
                if not self.solution:
                    print(solutions)
                    print(field)
                    self.solution = copy.deepcopy(solutions)
                    return 1
                else:
                    return 0
            if check == 0:
                return 0
            if check == 1:
                solutions.append([x_pos, y_pos])
                moves = KnightGame.get_available_moves_static(field, x_pos, y_pos, x_size, y_size)

                return sum([self.find_solution(copy.deepcopy(field), x[0], x[1], x_size, y_size, solutions) for x in moves])


first = KnightGame()

first.main_loop()
