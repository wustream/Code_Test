import numpy as np

def one_dim_center(x):
    l = len(x)
    if l%2 == 1: # odd number
        return int(l/2)
    else:
        if x[int(l/2-1)] > x[int(l/2)]:
            return int(l/2-1)
        else:
            return int(l/2)

def find_start(garden):
    """
    garden is a 2D array.
    n is the total length of
    """
    n = garden.shape[0]
    m = garden.shape[1]
    if n>=2 and m == 1:
        return(one_dim_center(garden[:,0]), 0)
    elif n==1 and m >= 2:
        return(0, one_dim_center(garden[0,:]))
    elif n==1 and m==1:
        return(0,0)
    else:
        if n%2 == 1 and m%2 == 1: # both odd number
            return(int((n-1)/2), int((m-1)/2))
        elif n%2 != 1 and m%2 == 1: # m is odd, center of m is fixed
            return(one_dim_center(garden[:, int((m-1)/2)]), int((m-1)/2))
        elif n%2 == 1 and m%2 != 1: # n is odd
            return(int((n-1)/2),one_dim_center(garden[(n-1)/2,:]))
        else: # both even number
            max_index = (int(n/2-1), int(m/2-1))
            for i in range(2):
                for j in range(2):
                    if garden[max_index] < garden[max_index[0]+i, max_index[1]+j]:
                        max_index = (max_index[0]+i, max_index[1]+j)
            return (max_index)

def check_max(x):
    """
    x is a list of numbers
    return the index of the maximum of x
    by default, return the min index if there is a tie
    """
    return(x.index(max(x)))

def return_max(garden, index_list):
    value_list =[garden[index] for index in index_list]
    if garden[index_list[check_max(value_list)]] == 0:
            return ('sleep')
    else:
        return (index_list[check_max(value_list)])

def corner_move(garden, x, y):
    if x == 0 and y == 0:
        # create a two list, one save the index, one save the value
        index_list = [(x, y+1), (x+1, y)]
        next_step = return_max(garden, index_list)
    elif x == 0 and y == garden.shape[1]-1:
        # create a two list, one save the index, one save the value
        index_list = [(x, y-1), (x+1, y)]
        next_step = return_max(garden, index_list)
    elif x == garden.shape[0]-1 and y == 0:
        # create a two list, one save the index, one save the value
        index_list = [(x, y+1), (x-1, y)]
        next_step = return_max(garden, index_list)
    elif x == garden.shape[0]-1 and y == garden.shape[1]-1:
        # create a two list, one save the index, one save the value
        index_list = [(x, y-1), (x-1, y)]
        next_step = return_max(garden, index_list)
    return(next_step)


def edge_move(garden, x, y):
    """
    if bunny is at the four edges, we need to check the sorrouning 3 cells.
    """
    if x == 0:
        # create a list to save the value and indices of the 3 cells
        index_list = [(x, y-1), (x+1, y), (x, y+1)]
        next_step = return_max(garden, index_list)
    elif x == garden.shape[0]-1:
        index_list = [(x, y-1), (x-1, y), (x, y+1)]
        next_step = return_max(garden, index_list)
    elif y == 0:
        index_list = [(x-1, y), (x, y+1), (x+1, y)]
        next_step = return_max(garden, index_list)
    else:
        index_list = [(x-1, y), (x, y-1), (x+1, y)]
        next_step = return_max(garden, index_list)
    return (next_step)

def inner_move(garden, x, y):
    """
    if bunny is at the four edges, we need to check the sorrouning 4 cells.
    """
    index_list = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    next_step = return_max(garden, index_list)
    return(next_step)

def at_corner(garden, x, y):
    """
    x, y is the location indices of the bunny
    """
    corner_index_list = [(0,0), (0,garden.shape[1]-1), (garden.shape[0]-1, 0), (garden.shape[0]-1, garden.shape[1]-1)]
    if (x,y) in corner_index_list:
        return True
    else:
        return False

def at_edge(garden, x, y):
    """
    x, y is the location indices of the bunny
    """
    if x==0 or y ==0 or x==garden.shape[0]-1 or y==garden.shape[1]-1:
        return True
    else:
        return False


def find_next_step(garden, x, y):
    """
    gargen is the current matrix having carrots
    x, y is the current location of the bunny
    """
    # 1. if at the four corners, 2 directions to check
    if at_corner(garden, x, y):
        return (corner_move(garden, x, y))
    # 2. if at the edge, 3 directions to check
    elif at_edge(garden, x, y):
        return (edge_move(garden, x, y))
    # 3. if in the innder, 4 directions to check
    else:
        return (inner_move(garden, x, y))

def bunny_move(garden, carrots, start_x, start_y):
    next_step = find_next_step(garden, start_x, start_y)
    if next_step == 'sleep':
        # if nother to eat, sleep and return total carrots
        return(carrots)
    else:
        # move to the next cell
        start_x, start_y = next_step
        # eat the carrots
        carrots = carrots+garden[start_x, start_y]
        garden[start_x, start_y] = 0
        print(carrots)
        print(start_x, start_y)
        # and move on
        return(bunny_move(garden, carrots, start_x, start_y))


def bunny(garden):
    """
    garden is a n*m matrix containing the number of carrots
    bunny will start from the center with highest number of carrots and move to the next highest
    one until fall asleep.
    return: total carrots that bunny eats
    """

    # 1. determine the starting point of the bunny
    # 1.1 for n and m, if both odd, use the index that has the highest value if odd.
    # 1.2 if n or m is odd, use the index of the odd one and use the max of middle two of
    # the even one
    # 1.3 if both n and m are odd, use the max of the middle 4.
    start_x, start_y = find_start(garden)
    # 2. eat the carrots in current cell
    carrots = garden[start_x, start_y]
    # 3. use recursive function to calculate the total carrots.
    carrots = bunny_move(garden, carrots, start_x, start_y)
    return (carrots)


garden1 = np.array(
    [[5, 7, 8, 6, 3],
     [1, 0, 7, 0, 4],
     [5, 0, 3, 4, 9],
     [0, 1, 0, 5, 8]])

bunny(garden1)