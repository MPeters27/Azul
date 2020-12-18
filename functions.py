def backward_induction(tree, path, link, active_player, actions):

    if type(link[0]) is not tuple:
        active_player += 1
        for entry in link:
            backward_induction(tree, path, tree[entry], active_player % 2, actions)
        active_player -= 1

    comparables = [number[active_player % 2] for number in link]
    winner = comparables.index(max(comparables))
    winning_tuple = link[winner]

    if len(tree) != 1:
        key_list = list(tree.keys())
        val_list = list(tree.values())
        findable = key_list[val_list.index(link)]
        # path[findable] = 'A' + str(winner)
        path[findable] = actions[int(findable)][winner]
        del tree[findable]
        val_list = list(tree.values())
        for X in val_list:
            for Y in X:
                if Y == findable:
                    key = str(key_list[val_list.index(X)])
                    modifiable = tree[key].index(Y)
        tree[key][modifiable] = winning_tuple

    else:

        comparables = [number[active_player % 2] for number in link]
        winner = comparables.index(max(comparables))
        winning_tuple = link[winner]
        path['0'] = 'A' + str(winner)
        path['0'] = actions[0][winner]
        return winning_tuple


def create_template_spne(width, depth):

    total_entries = 0
    tick = 0
    new_dict = {}

    while tick < depth:
        total_entries += width**tick
        tick += 1

    for i in range(total_entries):
        new_dict[str(i)] = 'E'

    return new_dict


def create_tree(tuple_list):
    return {'0': ['1', '2', '3'], '1': tuple_list[0], '2': tuple_list[1], '3': tuple_list[2]}

# Tree format: tuple_list = [[()()()][()()()][()()()]]

