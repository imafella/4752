from settings import *

# the class we will use to store the map, and make calls to path finding
class Grid:
    # set up all the default values for the frid and read in the map from a given file
    def __init__(self, filename):
        self.__values  = []         # rewards[row][col] = current value estimate for state (row,col)
        self.__rewards = []         # rewards[row][col] = reward obtained when state (row,col) reached
        self.__grid    = []         # grid[row][col]: 0 = WALKABLE, 1 = BLOCKED, 2 = TERMINAL
        self.__policy  = []         # policy[row][col][action] = probability of taking LEGAL_ACTIONS[action] at state (row,col)
        self.__rows    = 0          # number of rows in the grid
        self.__cols    = 0          # number of columns in the grid
        self.__load_data(filename)  # load the grid data from a given file
        self.__set_initial_values() # set the initial value estimate for the state
        self.__set_initial_policy() # set the initial policy estimate for the state

    def rows(self):                 return self.__rows
    def cols(self):                 return self.__cols
    def get_values(self):           return self.__values
    def get_state(self, r, c):      return self.__grid[r][c]
    def get_value(self, r, c):      return self.__values[r][c]
    def get_reward(self, r, c):     return self.__rewards[r][c]
    def get_policy(self, r, c):     return self.__policy[r][c]
    def get_min_value(self):        return min([min(col) for col in self.__values])
    def get_max_value(self):        return max([max(col) for col in self.__values])


    # loads the grid data from a given file name
    def __load_data(self, filename):
        # turn each line in the map file into a list of integers
        f = open(filename, 'r')
        for line in f:
            self.__grid.append([])
            self.__rewards.append([])
            l = line.strip().split(",")
            for c in l:
                c = c.strip()
                if c == 'X':    
                    self.__grid[-1].append(STATE_BLOCKED)
                    self.__rewards[-1].append(0)
                elif c == 'T':  
                    self.__grid[-1].append(STATE_TERMINAL)
                    self.__rewards[-1].append(0)
                else:       
                    self.__grid[-1].append(STATE_WALKABLE)    
                    self.__rewards[-1].append(0 if 'X' in c else float(c))
        # set the number of rows and columns of the file
        self.__rows, self.__cols = len(self.__grid), len(self.__grid[0])
        
    # sets the initial value estimate of the state so that each state has value 0
    def __set_initial_values(self):
        self.__values = [[0]*self.cols() for i in range(self.rows())]

    # sets the initial equiprobable policy for all states in the grid
    # you can use this as a template for how you implement the update_policy function below
    def __set_initial_policy(self):
        # our policy is a 3D array indexed by [row][col][action_index] where action_index is the index of LEGAL_ACTIONS
        initial_policy = [[[]]*self.cols() for i in range(self.rows())]
        # iterate through every row, col in the grid, setting the policy for that state
        for r in range(self.rows()):
            for c in range(self.cols()):
                # we have a null policy for the goal state because it's a terminal state, we can't move from it
                if self.get_state(r,c) != STATE_WALKABLE:
                    initial_policy[r][c] = [0]*len(LEGAL_ACTIONS)
                    continue
                # for every non-terminal state, set an equiprobable policy of moving in a legal direction
                # here, 'legal' will be an array of 1s and 0s, 1 indicating that LEGAL_ACTIONS[i] is legal
                legal = [1 if self.__is_legal_action(r, c, action) else 0 for action in LEGAL_ACTIONS]
                # we can sum the binary array to get the number of legal actions at this state
                num_legal = sum(legal)
                # so now the equiprobable policy is just dividing each element of the binary array by the number of actions
                state_policy = [i/num_legal for i in legal]
                # set the current policy
                initial_policy[r][c] = state_policy
        # set the class policy to this initial policy we just created
        self.__policy = initial_policy

    # check whether we can make a action from a given state
    def __is_legal_action(self, row, col, action):
        # check if the action will place us out of bounds
        new_row, new_col = row + action[0], col + action[1]
        # return false if the new row, col is off of the grid
        if new_row < 0 or new_col < 0 or new_row >= self.rows() or new_col >= self.cols(): return False
        # it's a legal action if the resulting state is 0 (not blocked)
        return self.get_state(new_row, new_col) != STATE_BLOCKED

    #
    # This function does a one-step value function estimation update using dynamic programming
    # The end result modifies only the self.__values structure to reflect the new value estimation

    #
    def update_values(self):


        #Creates and empty values table
        new_values = [[0 for i in range(self.__rows)] for j in range(self.__cols)]
        #For all states in grid
        for r in range(self.rows()):
            for c in range(self.cols()):
                #Skipps if state isnt walkable
                if self.get_state(r,c) != STATE_WALKABLE: continue
                #lists legal moves
                legal = [1 if self.__is_legal_action(r, c, action) else 0 for action in LEGAL_ACTIONS]
                for  a in range(4):
                    #if Move is not legal, Skip
                    if legal[a] == 0: continue
                    next_state = (r+LEGAL_ACTIONS[a][0], c+LEGAL_ACTIONS[a][1])
                    probability = self.__policy[r][c][a]
                    reward = self.get_reward(r,c)
                    new_values[r][c]+=  probability * (reward + RL_GAMMA * self.__values[next_state[0]][next_state[1]])
        self.__values = new_values



    #
    # This function should do a one-step value policy calculation update using dynamic programming
    # The end result should modify only the self.__policy structure to reflect the new policy

    def update_policy(self):
            for r in range(self.rows()):
                for c in range(self.cols()):
                    #states with a reward > 0 are skipped
                    if self.get_reward(r, c) > 0: continue
                    #a short list of all the legal moves
                    legal_states = []
                    legal = [1 if self.__is_legal_action(r, c, action) else 0 for action in LEGAL_ACTIONS]
                    for a in range(4):
                        if legal[a] > 0:
                            legal_states.append(self.get_value(r+LEGAL_ACTIONS[a][0], c+LEGAL_ACTIONS[a][1]))
                        else:
                            #if state isn't a legal move, it is an arbitrary low number
                            legal_states.append(-9999)

                    # calculates the total number of max value values in legal_states
                    total_maxs = 0
                    for i in range(4):
                        if legal_states[i] == max(legal_states):
                            total_maxs += 1
                    # blank policy because I keep breaking this program any other way.
                    p = [0.0, 0.0, 0.0, 0.0]
                    for i in range(4):
                        if legal_states[i] == max(legal_states):
                            p[i] = 1 / total_maxs

                    self.__policy[r][c] = p
    #


    # NOTE:
    #
    # - You can press the 's' key to do a value and policy iteration update step
    # - Holding the 's' key should do this a number of times
    # - Your algorithm should 'converge' (ie: stop changing values) to the shortest path policy
    # - When I grade your code, I will be checking that once your code has converged, that
    #   the policy you have generated is the same as the solution