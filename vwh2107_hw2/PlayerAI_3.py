#Vikram vwh2107
# PlayerAI_3 for homework2 2048 Artificial Intelligence

from BaseAI_3 import BaseAI
import time
import random
import math
import itertools

MAX_DEPTH = 4
timeLimit = 0.18
global prevTime

class PlayerAI(BaseAI):
    def getMove(self, grid):

        global prevTime
        # global m_d
        global MAX_DEPTH

        prevTime = time.process_time()
        # moveset = grid.getAvailableMoves()
        # while not terminalTest(grid, 0):
        #     pass
        #
        # return random.choice(moveset)[0]

        MAX_DEPTH = 4
        # m_d = 0
        # (child, _) = Maximize(grid.clone(), -float('inf'), float('inf'), 0)
        # #
        # return child[0]
        move = ids(grid)
        if move is None:
            moveset = grid.getAvailableMoves()
            return random.choice(moveset)[0]
        return move

# Iterative deepening search
def ids(grid):
    global MAX_DEPTH
    last_child = None
    while DecisionTime() is False:
        (child, _) = Maximize(grid, -float('inf'), float('inf'), 0)
        if child != None:
            last_child = child
        if MAX_DEPTH < 7:
            MAX_DEPTH = MAX_DEPTH + 3
    child = last_child
    if child is None:
        return None
    return child[0]


def DecisionTime():
    global prevTime
    return time.process_time() - prevTime > timeLimit


def terminalTest(grid, depth):
    if depth > MAX_DEPTH:
        return True
    if DecisionTime():
        return True
    if not grid.canMove():
        return True
    return False


def Eval(grid):

    smooth_weight = 1
    max_weight = 0

    smoothing = smoothHeuristics(grid)
    return smoothing
    #* smooth_weight + max_weight * math.log2(grid.getMaxTile())
           # math.log2(max(values))
    #return 4 * max(values) + 5 * penalty
    #math.log2(grid.getMaxTile())

    #return grid.getMaxTile() + len(grid.getAvailableCells())
def absSub(x,y):
    return abs(x-y)

def smoothHeuristics(grid):
    emptyCells = len(grid.getAvailableCells())
    h1 = emptyCells / (grid.size * grid.size)

    # Smoothness of tiles. Lower is better
    smooth = 0
    # Along each column
    for i in range(grid.size - 1):
        smooth += sum(list(map(absSub, grid.map[i], grid.map[i + 1])))
    # Along each row
    for i in range(grid.size):
        smooth += sum(list(map(absSub, grid.map[i][:-1], grid.map[i][1:])))

    emptyCells = sum(itertools.chain.from_iterable(grid.map))
    h2 = smooth / (2 * emptyCells)
    # Divided by 2 to ensure maximum normalised value is 1

    return h1 - h2

#Expected minimax with alpha-beta pruning

def expected(grid,alpha,beta,depth,position):
    if terminalTest(grid,depth):
        return None, Eval(grid)
    tileValues = [2, 4]
    expected_2 = 0
    expected_4 = 0
    for tile in tileValues:
        childGrid = grid.clone()
        childGrid.insertTile(position, tile)
        _, maxUtility = Maximize(childGrid, alpha, beta, depth)
        if tile is 2:
            expected_2 = 0.9 * maxUtility
        if tile is 4:
            expected_4 = 0.1 * maxUtility
    return  _, expected_2 + expected_4


def Minimize(grid, alpha, beta,depth):
    depth = depth + 1
    if terminalTest(grid,depth):
        return None, Eval(grid)

    (minChild, minUtility) = (None, float('inf'))

    tileValues = [2, 4]
    mylist = []
    for cellValue in tileValues:
        for cell in grid.getAvailableCells():
            mylist.append((cellValue, cell))

    for cell in grid.getAvailableCells():

        (_,utility) = expected(grid, alpha, beta, depth,cell)
        if utility < minUtility:
            (minChild, minUtility) = (cell, utility)

        if minUtility <= alpha:
            break

        if minUtility < beta:
            beta = minUtility

    return minChild, minUtility


def Maximize(grid, alpha, beta, depth):
    depth = depth + 1
    if terminalTest(grid,depth):
        return None, Eval(grid)

    (maxChild, maxUtility) = (None, -float('inf'))

    for child in grid.getAvailableMoves():
        (_, utility) = Minimize(child[1], alpha, beta, depth)

        if utility > maxUtility:
            (maxChild, maxUtility) = (child, utility)

        if maxUtility >= beta:
            break

        if maxUtility > alpha:
            alpha = maxUtility

    return maxChild, maxUtility

