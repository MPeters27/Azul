import numpy as np


class Tile:
    def __init__(self, color="blank"):
        self.color = color

    def __str__(self):
        return self.color


class Space:
    def __init__(self, status, color):
        self.status = status
        self.color = color

    def update_status(self):
        self.status = not self.status

    def __str__(self):
        return '('+str(self.status)+','+self.color+')'


class Wall:
    # placements is a 2D array of coordinates. For each coordinate, if it is True, that space is occupied when
    # initializing
    def __init__(self, placements, initial_score):

        self.score = initial_score
        self.evora = np.empty((5, 5), dtype=Space)

        for i in range(5):
            for j in range(5):
                if placements[i][j]:
                    self.evora[i][j] = Space(True, color='blank')
                else:
                    self.evora[i][j] = Space(False, color='blank')

        self.evora[0][0].color = 'blue'
        self.evora[0][1].color = 'yellow'
        self.evora[0][2].color = 'red'
        self.evora[0][3].color = 'black'
        self.evora[0][4].color = 'white'

        self.evora[1][0].color = 'white'
        self.evora[1][1].color = 'blue'
        self.evora[1][2].color = 'yellow'
        self.evora[1][3].color = 'red'
        self.evora[1][4].color = 'black'

        self.evora[2][0].color = 'black'
        self.evora[2][1].color = 'white'
        self.evora[2][2].color = 'blue'
        self.evora[2][3].color = 'yellow'
        self.evora[2][4].color = 'red'

        self.evora[3][0].color = 'red'
        self.evora[3][1].color = 'black'
        self.evora[3][2].color = 'white'
        self.evora[3][3].color = 'blue'
        self.evora[3][4].color = 'yellow'

        self.evora[4][0].color = 'yellow'
        self.evora[4][1].color = 'red'
        self.evora[4][2].color = 'black'
        self.evora[4][3].color = 'white'
        self.evora[4][4].color = 'blue'

    def tile_placement(self, row_number, color):
        # find slot that corresponds to the color we need
        spaces = self.evora[row_number-1]
        for i in range(5):
            if spaces[i].color == color:
                spaces[i].update_status()
                self.score += accumulate_score(row_number-1, i, self.evora, 0)

    def is_valid_placement(self, row_number, color):
        # needs testing
        spaces = self.evora[row_number - 1]
        flag = True
        for i in range(5):
            if spaces[i].color == color and spaces[i].status is True:
                flag = False
        return flag

    def rule_four(self, row_number, color):
        spaces = self.evora[row_number - 1]
        index = 0
        temp_score = 0
        for i in range(5):
            if spaces[i].color == color:
                index = i
        if index < 4:
            if spaces[index + 1].status is True:
                temp_score += 1
        if index > 0:
            if spaces[index - 1].status is True:
                temp_score += 1
        if row_number > 0:
            if self.evora[row_number - 2][index].status is True:
                temp_score += 1
        if row_number < 5:
            if self.evora[row_number][index].status is True:
                temp_score += 1

        return temp_score

    def rule_five(self, row_number, color):
        spaces = self.evora[row_number - 1]
        index = 0
        temp_score = 0
        for i in range(5):
            if spaces[i].color == color:
                index = i

        for i in range(5):
            if self.evora[i][index].status is True:
                temp_score += 1

        return temp_score

    def __str__(self):

        result = ''

        for i in range(5):
            result += "\n"
            for j in range(5):
                result += str(self.evora[i][j])
                result += ''

        return result


def accumulate_score(location_i, location_j, grid, score):
    # When i is 0, you can't go up. When i is 4, you can't go down.
    # When j is 0, you can't go left. When j is 4, you can't go right.
    # Will need to run more rigorous tests on this function
    horizontal_flag = False
    vertical_flag = False
    score += 1
    if location_j > 0:
        if grid[location_i][location_j-1].status is True:
            score = accumulate_score_left(location_i, location_j-1, grid, score)
            horizontal_flag = True
    if location_j < 4:
        if grid[location_i][location_j+1].status is True:
            score = accumulate_score_right(location_i, location_j+1, grid, score)
            horizontal_flag = True
    if location_i > 0:
        if grid[location_i-1][location_j].status is True:
            score = accumulate_score_up(location_i-1, location_j, grid, score)
            vertical_flag = True
    if location_i < 4:
        if grid[location_i+1][location_j].status is True:
            score = accumulate_score_down(location_i+1, location_j, grid, score)
            vertical_flag = True

    if horizontal_flag and vertical_flag:
        score += 1

    return score


def accumulate_score_left(location_i, location_j, grid, score):
    score += 1
    if location_j > 0:
        if grid[location_i][location_j-1].status is True:
            score = accumulate_score_left(location_i, location_j-1, grid, score)
    return score


def accumulate_score_right(location_i, location_j, grid, score):
    score += 1
    if location_j < 4:
        if grid[location_i][location_j+1].status is True:
            score = accumulate_score_right(location_i, location_j+1, grid, score)
    return score


def accumulate_score_up(location_i, location_j, grid, score):
    score += 1
    if location_i > 0:
        if grid[location_i-1][location_j].status is True:
            score = accumulate_score_up(location_i-1, location_j, grid, score)
    return score


def accumulate_score_down(location_i, location_j, grid, score):
    score += 1
    if location_i < 4:
        if grid[location_i+1][location_j].status is True:
            score = accumulate_score_down(location_i+1, location_j, grid, score)
    return score


class Slots:
    def __init__(self, capacity=1, occupation=0, color="blank"):
        self.color = color
        self.occupation = occupation
        self.capacity = capacity

    def modify(self, move_choice):
        self.occupation += len(move_choice)
        self.color = move_choice[0]

    def is_valid_modification(self, move_choice):
        if self.color == 'blank':
            return True
        elif self.color != move_choice[1][0]:
            return False
        elif self.capacity - self.occupation == 0:
            return False
        else:
            return True

    def is_full(self):
        if self.occupation == self.capacity:
            return True
        else:
            return False

    def empty(self):
        self.color = 'blank'
        self.occupation = 0

    def __str__(self):
        return self.color + ' ' + str(self.occupation) + '/' + str(self.capacity)


class PlayerRows:
    def __init__(self, occupation_colors):
        # provides an array of tuples that specify an occupation for each slot and a color
        self.S1 = Slots(1, occupation=occupation_colors[0][0], color=occupation_colors[0][1])
        self.S2 = Slots(2, occupation=occupation_colors[1][0], color=occupation_colors[1][1])
        self.S3 = Slots(3, occupation=occupation_colors[2][0], color=occupation_colors[2][1])
        self.S4 = Slots(4, occupation=occupation_colors[3][0], color=occupation_colors[3][1])
        self.S5 = Slots(5, occupation=occupation_colors[4][0], color=occupation_colors[4][1])

    def __str__(self):
        return str(self.S1) + '\n' + str(self.S2) + '\n' + str(self.S3) + '\n' + \
            str(self.S4) + '\n' + str(self.S5)


class PlayerCard:

    def __init__(self, player_rows, wall, overflow):
        self.score = wall.score
        self.rows = player_rows
        self.palace = wall
        self.overflow = overflow

    def is_valid_move(self, slot, move_choice):
        # needs testing
        s = [item for item in vars(self.rows).values()][slot-1]
        if s.is_valid_modification(move_choice) and self.palace.is_valid_placement(slot, move_choice[0]):
            return True
        else:
            return False

    def make_move(self, slot, move_choice):
        choice_slot = [item for item in vars(self.rows).values()][slot-1]

        while len(move_choice) > choice_slot.capacity - choice_slot.occupation:
            move_choice.pop()
            self.overflow.add()
        choice_slot.modify(move_choice)

    def wall_transfer(self):
        # transfer tiles in rows over to wall in order from top to bottom
        slots = [item for item in vars(self.rows).values()]
        for s in slots:
            if s.is_full():
                self.palace.tile_placement(s.capacity, s.color)
                s.empty()
        self.score = self.palace.score
        self.overflow.penalize()
        self.score += self.overflow.penalty
        self.overflow.empty()

    # rule function tests:
    def rule_one_check(self, move_choice, slot):
        s = [item for item in vars(self.rows).values()][slot - 1]
        if s.occupation + len(move_choice) == s.capacity:
            return True
        else:
            return False

    def rule_two_check(self, move_choice, slot):
        s = [item for item in vars(self.rows).values()][slot - 1]
        if slot == 3 and s.occupation + len(move_choice) == s.capacity:
            return True
        else:
            return False

    def rule_three_check(self, move_choice, slot):
        s = [item for item in vars(self.rows).values()][slot - 1]
        if (slot == 4 or slot == 5) and s.occupation + len(move_choice) == s.capacity:
            return True
        else:
            return False

    def rule_four_check(self, move_choice, slot):
        return self.palace.rule_four(slot, move_choice[0])

    def rule_five_check(self, move_choice, slot):
        s = [item for item in vars(self.rows).values()][slot - 1]
        if len(move_choice) + s.occupation > s.capacity:
            return True
        else:
            return False

    def rule_six_check(self, move_choice, slot):
        return self.palace.rule_five(slot, move_choice[0])

    def __str__(self):
        return "Score: \n\n" + str(self.score) + '\n\n' + "Rows: \n\n" + str(self.rows) + \
            '\n\n' + "Wall: \n" + str(self.palace)


class Washer:
    def __init__(self, color1='blank', color2='blank', color3='blank', color4='blank', wash_num=1):

        self.T1 = Tile(color1)
        self.T2 = Tile(color2)
        self.T3 = Tile(color3)
        self.T4 = Tile(color4)
        self.id_num = wash_num

        takes = []
        self.contents = [self.T1.color, self.T2.color, self.T3.color, self.T4.color]

        blue = [item for item in self.contents if item is 'blue']
        yellow = [item for item in self.contents if item is 'yellow']
        red = [item for item in self.contents if item is 'red']
        black = [item for item in self.contents if item is 'black']
        white = [item for item in self.contents if item is 'white']

        takes.append(blue)
        takes.append(yellow)
        takes.append(red)
        takes.append(black)
        takes.append(white)

        self.takes = [(self.id_num, item) for item in takes if len(item)]

    def outliers(self, player_choice):

        # exclude the one color in the player choice for the outliers
        color_choice = player_choice[0]
        return [item for item in self.contents if item != color_choice]

    def wash(self):

        self.T1.color = 'blank'
        self.T2.color = 'blank'
        self.T3.color = 'blank'
        self.T4.color = 'blank'
        self.takes = []

    def __str__(self):
        return str(self.T1) + ' ' + str(self.T2) + ' ' + str(self.T3) + ' ' + str(self.T4) + '\n' +\
               str(self.takes)


class Center:
    def __init__(self, center_num, *argv):

        self.id_num = center_num
        self.pool = []
        for arg in argv:
            self.pool.append(arg)

        takes = []

        blue = [item for item in self.pool if item is 'blue']
        yellow = [item for item in self.pool if item is 'yellow']
        red = [item for item in self.pool if item is 'red']
        black = [item for item in self.pool if item is 'black']
        white = [item for item in self.pool if item is 'white']

        takes.append(blue)
        takes.append(yellow)
        takes.append(red)
        takes.append(black)
        takes.append(white)

        self.takes = [(self.id_num, item) for item in takes if len(item)]

    def push(self, arg):
        self.pool.append(arg)

    def take_from_center(self, move_choice):
        color_choice = move_choice[0]
        self.pool = [item for item in self.pool if item != color_choice]

    def update_center_takes(self):

        takes = []

        blue = [item for item in self.pool if item is 'blue']
        yellow = [item for item in self.pool if item is 'yellow']
        red = [item for item in self.pool if item is 'red']
        black = [item for item in self.pool if item is 'black']
        white = [item for item in self.pool if item is 'white']

        takes.append(blue)
        takes.append(yellow)
        takes.append(red)
        takes.append(black)
        takes.append(white)

        self.takes = [(self.id_num, item) for item in takes if len(item)]

    def __str__(self):
        return "Contents: \n" + str(self.pool) + '\n' + "Takes: \n" + str(self.takes)


class Table:
    def __init__(self, w1, w2, w3, w4, w5, c):
        self.W1 = w1
        self.W2 = w2
        self.W3 = w3
        self.W4 = w4
        self.W5 = w5

        self.center = c

        self.W1takes = w1.takes
        self.W2takes = w2.takes
        self.W3takes = w3.takes
        self.W4takes = w4.takes
        self.W5takes = w5.takes
        self.Center_takes = c.takes

        self.all_takes = w1.takes + w2.takes + w3.takes + w4.takes + w5.takes + c.takes

    # process the player's move on the table by moving the outlying pieces on the choice washer to the center
    # of the table
    def transfer(self, washer, move_choice):
        if isinstance(washer, Center):
            self.center.take_from_center(move_choice)
            self.center.update_center_takes()
        else:
            outliers = washer.outliers(move_choice)
            for color in outliers:
                self.center.push(color)
            washer.wash()
            self.center.update_center_takes()

    def update_takes(self):
        self.W1takes = self.W1.takes
        self.W2takes = self.W2.takes
        self.W3takes = self.W3.takes
        self.W4takes = self.W4.takes
        self.W5takes = self.W5.takes
        self.Center_takes = self.center.takes
        self.all_takes = self.W1takes + self.W2takes + self.W3takes + self.W4takes + self.W5takes + self.Center_takes

    def is_round_over(self):
        if not self.all_takes:
            return True
        else:
            return False

    def __str__(self):
        return 'Washers:' + '\n \n' + str(self.W1) + '\n' + str(self.W2) + '\n' + str(self.W3) + '\n' + \
            str(self.W4) + '\n' + str(self.W5) + '\n' + str(self.center) + '\n'


class GameBoard:

    # we currently seem to have the functionality to say whether a move is valid and to make that move in entirety

    def __init__(self, t, p1, p2):
        # a player card has a set of player rows and a wall to place tiles on
        # the table has the washers and the table center
        self.table = t
        self.Player1 = p1
        self.Player2 = p2
        self.turn = True

    def __str__(self):
        return str(self.table) + '\n' + "Player 1: \n\n" + str(self.Player1) + \
            '\n\n' + "Player 2: \n\n" + str(self.Player2)

    def is_valid_turn(self, washer_choice, move_choice, slot):
        # need to check that the move is available from the washer of choice
        # need to check that the slot can be filled with that move via player card
        if self.turn:
            player = self.Player1
        else:
            player = self.Player2

        target_washer = [item for item in vars(self.table).values()][washer_choice - 1]
        if player.is_valid_move(slot, move_choice) and move_choice in target_washer.takes:
            return True
        else:
            return False

    # to make a move, we need to know whose turn it is, what washer they want to take from,
    # what tiles they want to take, and which slot they want to put the pieces on
    def make_turn(self, washer_choice, move_choice, slot):
        if self.turn:
            player = self.Player1
        else:
            player = self.Player2

        # modify the table
        if slot == 6:
            for i in range(len(move_choice)):
                player.overflow.add()
            self.table.center.pool.remove('yellow')
            self.table.center.update_center_takes()
            self.table.update_takes()
            self.turn = not self.turn
        else:
            target_washer = [item for item in vars(self.table).values()][washer_choice-1]
            self.table.transfer(target_washer, move_choice)
            self.table.update_takes()
            # modify the player card
            player.make_move(slot, move_choice)
            # change the current turn
            self.turn = not self.turn

    def round_end(self):
        # need to transfer tiles over to each player's wall and add up the points
        self.Player1.wall_transfer()
        self.Player2.wall_transfer()

    def move_enumeration(self):
        # returns all possible moves the current player can make
        w = [item for item in vars(self.table).values()]
        w = w[6:-1]
        tile_moveset = []
        for M in w:
            for N in M:
                tile_moveset.append(N)

        if self.turn:
            player = self.Player1
        else:
            player = self.Player2

        all_moves = []
        slots = [item for item in vars(player.rows).values()]
        for i in range(len(tile_moveset)):
            for j in range(len(slots)):
                if slots[j].is_valid_modification(tile_moveset[i]) and \
                        player.palace.is_valid_placement(j+1, tile_moveset[i][1][0]):
                    # input a move and the color of that move
                    all_moves.append((tile_moveset[i][0], tile_moveset[i][1], j+1))

        return all_moves


class Overflow:
    def __init__(self, amount=0):
        self.amount = amount
        self.penalty = 0

    def penalize(self):
        if self.amount < 3:
            self.penalty += self.amount*(-1)
        elif self.amount < 6:
            self.penalty += (self.amount - 2)*(-2) + (-2)
        elif self.amount < 8:
            self.penalty += (self.amount - 5)*(-3) + (-6) + (-2)

    def add(self):
        self.amount += 1

    def empty(self):
        self.amount = 0

    def __str__(self):
        return "Amount: " + str(self.amount) + " \nPenalty: " + str(self.penalty)


# need helper function that takes a move and assigns a value for how powerful it is
def rule_rationality_ranking(move, game_board, active_player):

    move_score = 0
    player = game_board.Player1
    if active_player != 0:
        player = game_board.Player2

    if player.rule_one_check(move[1], move[2]) is True:
        move_score += 1
    if player.rule_two_check(move[1], move[2]) is True:
        move_score += 2
    if player.rule_three_check(move[1], move[2]) is True:
        move_score += 3
    move_score += player.rule_four_check(move[1], move[2])
    if player.rule_five_check(move[1], move[2]) is True:
        move_score -= 2
    # move_score += player.rule_six_check(move[1], move[2])

    return move_score, move


def top_three(moveset, game_board, active_player):

    score_list = []
    for X in moveset:
        score_list.append(rule_rationality_ranking(X, game_board, active_player))

    the_best = sorted(score_list, reverse=True)[:3]
    return the_best
















