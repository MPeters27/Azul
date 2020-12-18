from stuff import *
from functions import *
import numpy as np
import copy

# initialize wall and rows for both players
truth_grid_p1 = np.empty((5, 5), dtype=Space)
truth_grid_p2 = np.empty((5, 5), dtype=Space)
for i in range(5):
    for j in range(5):
        truth_grid_p1[i][j] = False
        truth_grid_p2[i][j] = False

truth_grid_p1[0][1] = True
truth_grid_p1[0][2] = True
truth_grid_p1[1][1] = True
truth_grid_p1[2][2] = True
truth_grid_p1[2][3] = True
truth_grid_p1[3][1] = True
truth_grid_p1[4][4] = True

truth_grid_p2[0][1] = True
truth_grid_p2[0][2] = True
truth_grid_p2[1][1] = True
truth_grid_p2[2][0] = True
truth_grid_p2[2][1] = True


occupation_colors_p1 = [(0, 'blank'), (1, 'white'), (0, 'blank'), (0, 'blank'), (0, 'blank')]
occupation_colors_p2 = [(0, 'blank'), (1, 'yellow'), (0, 'blank'), (3, 'white'), (2, 'red')]

wall_p1 = Wall(truth_grid_p1, 10)
wall_p2 = Wall(truth_grid_p2, 10)
rows_p1 = PlayerRows(occupation_colors_p1)
rows_p2 = PlayerRows(occupation_colors_p2)
overflow_p1 = Overflow()
overflow_p2 = Overflow()

# initialize washers and center
washer1 = Washer('black', 'black', 'red', 'yellow', 1)
washer2 = Washer('black', 'red', 'blue', 'white', 2)
washer3 = Washer('black', 'black', 'blue', 'yellow', 3)
washer4 = Washer('white', 'white', 'red', 'red', 4)
washer5 = Washer('red', 'white', 'white', 'blue', 5)
center = Center(6)
table = Table(washer1, washer2, washer3, washer4, washer5, center)

# initialize player cards and the entire game board
p1 = PlayerCard(rows_p1, wall_p1, overflow_p1)
p2 = PlayerCard(rows_p2, wall_p2, overflow_p2)

A = GameBoard(table, p1, p2)

# Sample round. Players take turns until all washers and the center are empty
# Once everything is empty, tiles are transferred over to each player's wall
# and points are tallied


# returns a dynamic game subtree for the given game given the current player
def foresight(a, active_player):

    a_move_enumeration = a.move_enumeration()
    a_top_three = top_three(a_move_enumeration, a, active_player)

    #######################################################

    b1 = copy.deepcopy(a)
    b2 = copy.deepcopy(a)
    b3 = copy.deepcopy(a)

    b1.make_turn(a_top_three[0][1][0], a_top_three[0][1][1], a_top_three[0][1][2])
    b2.make_turn(a_top_three[1][1][0], a_top_three[1][1][1], a_top_three[1][1][2])
    b3.make_turn(a_top_three[2][1][0], a_top_three[2][1][1], a_top_three[2][1][2])

    b1_move_enumeration = b1.move_enumeration()
    b2_move_enumeration = b2.move_enumeration()
    b3_move_enumeration = b3.move_enumeration()
    b1_top_three = top_three(b1_move_enumeration, b1, 1)
    b2_top_three = top_three(b2_move_enumeration, b2, 1)
    b3_top_three = top_three(b3_move_enumeration, b3, 1)

    score1 = a_top_three[0][0]
    score2 = b1_top_three[0][0]
    score3 = a_top_three[0][0]
    score4 = b1_top_three[1][0]
    score5 = a_top_three[0][0]
    score6 = b1_top_three[2][0]

    score7 = a_top_three[1][0]
    score8 = b2_top_three[0][0]
    score9 = a_top_three[1][0]
    score10 = b2_top_three[1][0]
    score11 = a_top_three[1][0]
    score12 = b2_top_three[2][0]

    score13 = a_top_three[2][0]
    score14 = b3_top_three[0][0]
    score15 = a_top_three[2][0]
    score16 = b3_top_three[1][0]
    score17 = a_top_three[2][0]
    score18 = b3_top_three[2][0]

    a_action_list = [item[1] for item in a_top_three]
    b1_action_list = [item[1] for item in b1_top_three]
    b2_action_list = [item[1] for item in b2_top_three]
    b3_action_list = [item[1] for item in b3_top_three]

    scores = [[(score1, score2), (score3, score4), (score5, score6)], [(score7, score8), (score9, score10),
              (score11, score12)], [(score13, score14), (score15, score16), (score17, score18)]]
    the_tree = create_tree(scores)

    return the_tree, a_action_list, b1_action_list, b2_action_list, b3_action_list


def progress_game(a, active_player):

    foresight_results = foresight(a, active_player)
    tree = foresight_results[0]
    action_list = []
    for item in foresight_results[1:]:
        action_list.append(item)

    spne = create_template_spne(3, 2)
    result = backward_induction(tree, spne, tree['0'], active_player, action_list)

    a.make_turn(spne['0'][0], spne['0'][1], spne['0'][2])

    print(spne)


progress_game(A, 0)
progress_game(A, 1)
progress_game(A, 0)
progress_game(A, 1)
progress_game(A, 0)
progress_game(A, 1)

print(A)

A.make_turn(6, ['red', 'red', 'red', 'red', 'red'], 5)
A.make_turn(6, ['yellow'], 6)
A.make_turn(6, ['black', 'black', 'black'], 1)
A.round_end()
# progress_game(A, 0, False)
# progress_game(A, 1)W

print(A)

# print(rule_rationality_ranking((5, ['white', 'white'], 3), A, 0))
# print(top_three(A_move_enumeration, A, 0))


# G1 = GameBoardInstance(A, (5, ['white', 'white'], 3))
# G2 = GameBoardInstance(A, (4, ['white', 'white'], 3))
# G3 = GameBoardInstance(A, (2, ['white'], 3))

# A.make_turn(2, ['white'], 4)

# A.round_end()

# need to implement functionality to rank moves on any given turn, and choose the W best moves

