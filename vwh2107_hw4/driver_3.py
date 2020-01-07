#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def isComplete(assignment, vars):
    return set(assignment.keys()) == set(vars)


def mrv(assignment, csp, values):
    unassigned_variables = dict((squares, len(values[squares])) for squares in values if squares not in assignment.keys())
    mrv = min(unassigned_variables, key=unassigned_variables.get)
    return mrv


def fc(csp, values, assignment, var, value):
    values[var] = value
    for neighbor in csp[var]:
        values[neighbor] = values[neighbor].replace(value, '')


def cross(A, B):
    return [a+b for a in A for b in B]


def isConsistent(var, value, assignment, csp):
    for neighbor in csp[var]:
        if neighbor in assignment.keys() and assignment[neighbor]==value:
            return False

    return True


def Inference(assignment, inferences, csp, values, var, value):
    inferences[var] = value

    for neighbor in csp[var]:
        if neighbor not in assignment and value in values[neighbor]:
            if len(values[neighbor]) == 1:
                return "FAILURE"

            remaining = values[neighbor] = values[neighbor].replace(value, "")

            if len(remaining) == 1:
                flag = Inference(assignment, inferences, csp, values, 
                                 neighbor, remaining)
                if flag == "FAILURE":
                    return "FAILURE"

    return inferences


def backtrack(assignment, csp, values):
    from copy import deepcopy
    if isComplete(assignment, csp.keys()):
        return assignment

    var = mrv(assignment, csp, values)
    domain = deepcopy(values)

    for value in values[var]:
        if isConsistent(var, value, assignment, csp):
            assignment[var] = value
            inferences = {}
            inferences = Inference(assignment, inferences, csp, values, var, value)
            if inferences != "FAILURE":
                result = backtrack(assignment, csp, values)
                if result != "FAILURE":
                    return result

            del assignment[var]
            values.update(domain)

    return "FAILURE"


def backtracking(board):
    global ROW, COL
    """Takes a board and returns solved board."""

    csp = {x: set() for x in board.keys()}
    values = {x: '123456789' for x in board.keys()}
    unitlist = ([cross(ROW, c) for c in COL] +
                [cross(r, COL) for r in ROW] +
                [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')])

    units = dict((s, [u for u in unitlist if s in u]) for s in board.keys())

    for key in csp.keys():
        for unit in units[key]:
            for square in unit:
                if square != key:
                    csp[key].add(square)

        for const in csp[key]:
            if board[const] != 0:
                if str(board[const]) in values[key]:
                    values[key] = values[key].replace(str(board[const]), '')
                values[const] = str(board[const])

    solved_board = backtrack({}, csp, values)

    return solved_board


if __name__ == '__main__':
    #  Read boards from source.
    src_filename = 'sudokus_start.txt'
    try:
        srcfile = open(src_filename, "r")
        sudoku_list = srcfile.read()
    except:
        print("Error reading the sudoku file %s" % src_filename)
        exit()

    # Setup output file
    out_filename = 'output.txt'
    outfile = open(out_filename, "w")
    
    # Solve each board using backtracking
    for line in sudoku_list.split("\n"):

        if len(line) < 9:
            continue

        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(line[9*r+c])
                  for r in range(9) for c in range(9)}

        # Print starting board. TODO: Comment this out when timing runs.
        #print_board(board)

        # Solve with backtracking
        solved_board = backtracking(board)

        # Print solved board. TODO: Comment this out when timing runs.
        #print_board(solved_board)

        # Write board to file
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    print("Finishing all boards in file.")

