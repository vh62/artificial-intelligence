from __future__ import division
from __future__ import print_function

import sys
import math
import time
import heapq as hq
#import heapq as hq
from collections import deque

#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        
        # Get the index and (row, col) of empty block
        for i, item in enumerate(self.config):
            if item == 0:
                self.blank_row =int(i/self.n)
                self.blank_col =int(i % self.n)
                break

    def display(self):
        """ Display this Puzzle state as a n*n board """
        
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])
    
       
    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_row == 0:
                return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index - self.n
            new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(tuple(new_config),self.n,parent=self,action="Up",cost = self.cost +1)
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_row == self.n -1:
                return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + self.n
            new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_col == 0:
                return None    
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index -1
            new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_col == self.n - 1:
                return None
        else:
            blank_index = self.blank_row * self.n + self.blank_col
            target = blank_index + 1
            new_config = list(self.config)
        new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
        return PuzzleState(tuple(new_config), self.n, parent = self, action = "Right" ,cost = self.cost +1)

      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
    
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()
            ]
        
        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state, count, max_search_depth):
    ### Student Code Goes here
    """
    path_to_goal = get_path_to_goal(state)
    print ("path_to_goal:",path_to_goal)
    print ("cost_of_path:" ,(len(path_to_goal)))
    print ("nodes_expanded %d " % count)
    print ("search_depth %d " %  state.cost)
    print ("max_search_depth %d" % max_search_depth)

    """
    f = open("output.txt", "w+")

    path = get_path_to_goal(state)
    f.write( "path_to_goal: %s\n" % str(path) )
    f.write( "cost_of_path: %d\n" % len(path) )
    f.write( "nodes_expanded: %d\n" % count )
    f.write( "search_depth: %d\n" % state.cost )
    f.write( "max_search_depth: %d\n" % max_search_depth )
    f.close()

    
def get_path_to_goal(state):
    path_of_actions = []
    while( state.parent != None):
        path_of_actions.append(state.action)
        state = state.parent
    
    return path_of_actions[::-1]

def bfs_search(initial_state):
    """BFS search"""
    
    ### STUDENT CODE GOES HERE ###
    frontier = deque()
    frontier.append(initial_state)
    explored = set()
    node_count = 0;
    max_search_depth = 0;

    while len(frontier):
        state = frontier.popleft()
        boards_str = ''.join(map(str, state.config))
        explored.add(boards_str) 

        if test_goal(state):
            return state , node_count , max_search_depth
        node_count +=1
        children = state.expand()
        if children[0].cost > max_search_depth: max_search_depth = children[0].cost
        for i in children:
                child_str = ''.join(map(str, i.config))
                if  child_str not in explored:
                    frontier.append(i)
                    explored.add(child_str)

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###

    frontier = deque()
    frontier.append(initial_state)
    explored = set()
    node_count = 0
    max_search_depth = 0
    
    while len(frontier):
        state = frontier.pop()
        explored.add(''.join(map(str, state.config)))
        if state.cost > max_search_depth: max_search_depth = state.cost

        if test_goal(state):
            return state, node_count , max_search_depth

        children = state.expand()
        node_count += 1
        #checking from the back
        #for i in range(0, len(children), 1):
        for i in range(len(children)-1, -1, -1):
            child_str = ''.join(map(str, children[i].config))
            if child_str not in explored:
                frontier.append(children[i])
                explored.add(child_str)

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    
    frontier = []
    hq.heappush(frontier, (calculate_total_cost(initial_state), initial_state))
    explored = set([])
    
    nodes_count = 0
    max_search_depth = 0

    while len(frontier):
        cost, state = hq.heappop(frontier)
        #explored.add(state)
        explored.add(''.join(map(str, state.config)))
        if test_goal(state):
            return state, nodes_count, max_search_depth

        nodes_count += 1
        children = state.expand()

        if children[0].cost > max_search_depth: max_search_depth = children[0].cost
        for i in children:
            child_str = ''.join(map(str, i.config))
            if  child_str not in explored:
                hq.heappush(frontier, (calculate_total_cost(i), i)) 
                explored.add(child_str)

    
def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    total_manhattan_distance = 0
    for i in range(len(state.config)):
        if state.config[i] != 0:
            sum = calculate_manhattan_dist( i, state.config[i], state.n )
            total_manhattan_distance += sum
    return total_manhattan_distance + state.cost



def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    i_pos = idx / n
    j_pos = idx % n
    i_val = value / n
    j_val = value % n

    return abs(i_pos - i_val) + abs(j_pos - j_val)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    return ''.join(map(str, puzzle_state.config)) == "012345678"
    

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": 
        state, node_count, max_search_depth = bfs_search(hard_state)
    elif search_mode == "dfs": 
        state, node_count, max_search_depth = dfs_search(hard_state)
    elif search_mode == "ast": 
        state, node_count, max_search_depth = A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
    
    end_time = time.time()
    writeOutput(state, node_count, max_search_depth)
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
