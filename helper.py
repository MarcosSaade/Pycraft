import math


def sum_array(a, b):
    return [a[0] + b[0], a[1] + b[1]]


def idx_to_pos(idx):
    x = idx[0]
    y = idx[1]

    pos = [0, 0]

    pos[0] = 50 * x
    pos[1] = 550 - (y * 50)

    return pos


def print_world(world):
    counter = -1
    for col in world:
        counter += 1
        print(col)
        if counter == 15:
            print('-' * 100)
            counter = -1
    print('END', '*' * 100, 'END')


def p_board_y(pos):
    coor = [0, 0]

    y = (-pos[1] - (-11 * 50))

    coor[0] = round(pos[0] / 50)
    coor[1] = round(y / 50)

    return coor


def p_board_x(pos, dir):
    coor = [0, 0]

    y = (-pos[1] - (-11 * 50))

    if dir == 0:
        coor[0] = math.floor((pos[0] - 14) / 50)
    elif dir == 1:
        coor[0] = math.floor((pos[0] + 46 ) / 50)

    coor[1] = math.floor(y / 50)

    return coor


def coor_to_pos(coor):
    return [int(coor[0] / 50), int(coor[1] / 50)]
