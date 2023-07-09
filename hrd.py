from copy import deepcopy
from heapq import heappush, heappop
import time
import argparse
import sys

#fixed the f f value after heapop implemented

#====================================================================================

char_goal = '1'
char_single = '2'

class Piece:
    """
    This represents a piece on the Hua Rong Dao puzzle.
    """

    def __init__(self, is_goal, is_single, coord_x, coord_y, orientation):
        """
        :param is_goal: True if the piece is the goal piece and False otherwise.
        :type is_goal: bool
        :param is_single: True if this piece is a 1x1 piece and False otherwise.
        :type is_single: bool
        :param coord_x: The x coordinate of the top left corner of the piece.
        :type coord_x: int
        :param coord_y: The y coordinate of the top left corner of the piece.
        :type coord_y: int
        :param orientation: The orientation of the piece (one of 'h' or 'v') 
            if the piece is a 1x2 piece. Otherwise, this is None
        :type orientation: str
        """

        self.is_goal = is_goal
        self.is_single = is_single
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.orientation = orientation

    def __repr__(self):
        return '{} {} {} {} {}'.format(self.is_goal, self.is_single, \
            self.coord_x, self.coord_y, self.orientation)

class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, pieces):
        """
        :param pieces: The list of Pieces
        :type pieces: List[Piece]
        """

        self.width = 4
        self.height = 5

        self.pieces = pieces

        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        self.grid = []
        self.__construct_grid()


    def __construct_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """

        for i in range(self.height):
            line = []
            for j in range(self.width):
                line.append('.')
            self.grid.append(line)

        for piece in self.pieces:
            if piece.is_goal:
                self.grid[piece.coord_y][piece.coord_x] = char_goal
                self.grid[piece.coord_y][piece.coord_x + 1] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x] = char_goal
                self.grid[piece.coord_y + 1][piece.coord_x + 1] = char_goal
            elif piece.is_single:
                self.grid[piece.coord_y][piece.coord_x] = char_single
            else:
                if piece.orientation == 'h':
                    self.grid[piece.coord_y][piece.coord_x] = '<'
                    self.grid[piece.coord_y][piece.coord_x + 1] = '>'
                elif piece.orientation == 'v':
                    self.grid[piece.coord_y][piece.coord_x] = '^'
                    self.grid[piece.coord_y + 1][piece.coord_x] = 'v'

    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()
        

class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, f, depth, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param f: The f value of current state. //for A*
        :type f: int
        :param depth: The depth of current state in the search tree.
        :type depth: int
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.f = f
        self.depth = depth
        self.parent = parent
        #self.id = hash(board)  # The id for breaking ties.
        self.id = hash_board_config(board)  # Glen 's modifed self.id, original code right above

    #def __eq__(self, other):
    #    return self.f == other.f
    
    def __lt__(self, other):
        return self.f < other.f


def read_from_file(filename):
    """
    Load initial board from a given file.

    :param filename: The name of the given file.
    :type filename: str
    :return: A loaded board
    :rtype: Board
    """

    puzzle_file = open(filename, "r")

    line_index = 0
    pieces = []
    g_found = False

    for line in puzzle_file:

        for x, ch in enumerate(line):

            if ch == '^': # found vertical piece
                pieces.append(Piece(False, False, x, line_index, 'v'))
            elif ch == '<': # found horizontal piece
                pieces.append(Piece(False, False, x, line_index, 'h'))
            elif ch == char_single:
                pieces.append(Piece(False, True, x, line_index, None))
            elif ch == char_goal:
                if g_found == False:
                    pieces.append(Piece(True, False, x, line_index, None))
                    g_found = True
        line_index += 1

    puzzle_file.close()

    board = Board(pieces)
    
    return board


#glen's function
def hash_board_config(board):
    #print('during hash_board_config, the board is:' )
    #board.display()
    s = str(board.grid)
    #board_hash_id = hash(s)
    board_hash_id = s
    #print('during hash_board_config, board_hash_id: ', board_hash_id)
    #if board_hash_id == board_hash_id:
        #print('Red Flagged!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ')
    return board_hash_id


def is_explored(curr, explored):
    #print('during the is_explored, the curr.id is : ', curr.id)
    for i in explored:
        #use the self.id = hash(board) to check if two boards have the same configuration
        if i.id == curr.id:
            print('when matched in is_explored, the i.id is : ', i.id)
            return True
    return False

def is_id_explored(curr_id, explored_ids):
    #print('during the is_id_explored, the curr_id is : ', curr_id)
    for i in explored_ids:
        #use the self.id = hash(board) to check if two boards have the same configuration
        if i == curr_id:
            print('when matched in is_explored_ids, the id is : ', i)
            return True
    return False

#need helper function to check if this board config is the same as goal board config, deep board compare
def is_at_goal(curr):
    if curr.board.grid[4][1] == '1' and curr.board.grid[4][2] == '1':
        return True
    else:
        return False 



def create_a_successor(curr, empty_y, empty_x, piece_y, piece_x, d, shape ):
    #successor = deepcopy(curr)
    #some improvement I should try to improve speed, deepcopy the pieces instead of the board
    #deepcopied_board = deepcopy(curr.board)
    deepcopied_pieces = deepcopy(curr.board.pieces)
    new_identical_board = Board(deepcopied_pieces)
    successor = State( new_identical_board, 0, 0, curr)
    #successor = State( deepcopied_board, 0, 0, curr)
    #both pieces and grid are needed to be edited, but grid can be edited by calling _contruct_grid
    #edit the pieces
    for p in successor.board.pieces:
        if (d=='up' or d=='down' or d=='left' or d=='right') and shape=='2' and p.is_single==True and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif d=='up' and shape=='v'and p.orientation=='v' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y - 1
            p.coord_x = empty_x
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif d=='down' and shape=='v' and p.orientation=='v' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif d=='left' and shape=='h' and p.orientation=='h' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x - 1
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif d=='right' and shape=='h' and p.orientation=='h' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif (d=='left' or d=='right') and shape=='v' and p.orientation=='v' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif d=='left' and shape=='1' and p.is_goal==True and p.coord_y==piece_y and p.coord_x==piece_x: #8
            p.coord_y = empty_y
            p.coord_x = empty_x-1
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif d=='right' and shape=='1' and p.is_goal==True and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
            #successor.id = hash_board_config(successor.board)
            #successor.parent = curr
        elif (d=='up' or d=='down') and shape=='h' and p.orientation=='h' and p.coord_y==piece_y and p.coord_x==piece_x: #11 and #14
            p.coord_y = empty_y
            p.coord_x = empty_x
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif d=='up' and shape=='1' and p.is_goal==True and p.coord_y==piece_y and p.coord_x==piece_x: #12
            p.coord_y = empty_y-1
            p.coord_x = empty_x
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
        elif d=='down' and shape=='1' and p.is_goal==True and p.coord_y==piece_y and p.coord_x==piece_x: #13
            p.coord_y = empty_y
            p.coord_x = empty_x
            #successor.parent = curr
            #successor.id = hash_board_config(successor.board)
    #successor.parent = curr   
    successor.board.grid = []
    successor.board._Board__construct_grid()
    #successor.board.display()
    successor.id = hash_board_config(successor.board) 
    #debuging below:
    #successor.board.display()
    '''
    if successor.board.grid == [['.','.','<','>'],['1','1','^','2'],['^','1','v','2'],['v','^','2','2'],['.','v','<','>']]:
        print('Red Flagged!!!!!!!!!!!!!!!!!!!!!  current d is: ', d, 'current shape is:', shape)
    if successor.board.grid == [['<','>','^','2'],['1','1','v','2'],['1','1','.','2'],['^','^','.','2'],['v','v','<','>']]:
        print('Red Flagged!!!!!!!!!!!!!!!!!!!!!  current d is: ', d, 'current shape is:', shape)
    print(' ~ ')
    '''
    return successor


def add_curr_succ_to_frontier(curr, frontier):
    #print('Below is the current config:----------------------------------------------')
    #curr.board.display()
    #print('child of the current below---------------------------------------------------------------------------------------')
    direction = ['up', 'down', 'left', 'right']
    empty_squares = []
    y_coord = 0
    #print('add_curr_succ_to_frontier')
    for y in curr.board.grid: #start with y-axis
        x_coord = 0
        #debuging: print("y loop:" + str(y_coord))
        for x in y: #then x-axis
            if x == '.':
                empty_squares.append([y_coord, x_coord]) #will be used for cheking if two . are next to each other
                for d in direction:
                    if d == 'up' and (y_coord-1) >= 0 and curr.board.grid[y_coord-1][x_coord] == '2': # there can be movemnent for piece '2'
                        successor = create_a_successor(curr, y_coord, x_coord,(y_coord-1),x_coord, 'up', '2' )
                        frontier.append(successor)
                        #if(successor.id != curr.id):
                        #    frontier.append(successor)
                    elif d == 'up' and (y_coord-2) >= 0 and curr.board.grid[y_coord-1][x_coord] == 'v': # there can be movemnent for piece 'v'
                        successor = create_a_successor(curr, y_coord, x_coord,(y_coord-2),x_coord, 'up','v' )
                        frontier.append(successor)
                        #if(successor.id != curr.id):
                        #    frontier.append(successor)
                    elif d == 'down' and (y_coord+1) <= 4 and curr.board.grid[y_coord+1][x_coord] == '2': # there can be movemnent for piece '2'
                        successor = create_a_successor(curr, y_coord, x_coord,(y_coord+1),x_coord, 'down', '2' ) #this line cuz rasing errors!!!
                        frontier.append(successor)
                        #if(successor.id != curr.id):
                        #    frontier.append(successor)
                    elif d == 'down' and (y_coord+2) <= 4 and curr.board.grid[y_coord+1][x_coord] == '^': # there can be movemnent for piece 'v'
                        successor = create_a_successor(curr, y_coord, x_coord,(y_coord+1),x_coord, 'down','v' )
                        frontier.append(successor)
                        #if(successor.id != curr.id):
                        #    frontier.append(successor)
                    elif d == 'left' and (x_coord-1) >= 0 and curr.board.grid[y_coord][x_coord-1] == '2': # there can be movemnent for piece '2'
                        successor = create_a_successor(curr, y_coord, x_coord,y_coord, (x_coord-1), 'left', '2' )
                        frontier.append(successor)
                        #if(successor.id != curr.id):
                        #    frontier.append(successor)
                    elif d == 'left' and (x_coord-2) >= 0 and curr.board.grid[y_coord][x_coord-1] == '>': # there can be movemnent for piece 'v'
                        successor = create_a_successor(curr, y_coord, x_coord,(y_coord), (x_coord-2), 'left','h' )
                        frontier.append(successor)
                        #if(successor.id != curr.id):
                        #    frontier.append(successor)
                    elif d == 'right' and (x_coord+1) <= 3 and curr.board.grid[y_coord][x_coord+1] == '2': # there can be movemnent for piece '2'
                        successor = create_a_successor(curr, y_coord, x_coord,y_coord, (x_coord+1), 'right', '2' )
                        frontier.append(successor)
                        #if(successor.id != curr.id):
                        #    frontier.append(successor)
                    elif d == 'right' and (x_coord+2) <= 3 and curr.board.grid[y_coord][x_coord+1] == '<': # there can be movemnent for piece 'v'
                        successor = create_a_successor(curr, y_coord, x_coord,y_coord, (x_coord+1), 'right','h' )
                        frontier.append(successor)
                        #if(successor.id != curr.id):
                        #    frontier.append(successor)
            #debuging: print(x_coord)
            x_coord += 1
        
        y_coord += 1
    #now need to check if the two empty square is next to each other
    first_empty = empty_squares[0]
    second_empty = empty_squares[1]
    #first_empty[0] is y coordinate, first_empty[1] is x coordinate
    if ((first_empty[0]+1 == second_empty[0]) and (first_empty[1] == second_empty[1])) or ((first_empty[0]-1 == second_empty[0]) and (first_empty[1] == second_empty[1])): #vertical empty column
        #do: create_a_successor for the horizontal movement
        empty_col_y = min(first_empty[0], second_empty[0])
        empty_col_x = first_empty[1]
        for d in direction:
            #//3:02 AM Feb 3rd take a break now to get popeye continue from here
            if d == 'left' and (empty_col_x-1) >= 0 and curr.board.grid[empty_col_y][empty_col_x-1] == '^': # there can be movemnent for piece 'v'
                successor = create_a_successor(curr, empty_col_y, empty_col_x,(empty_col_y), (empty_col_x-1), 'left','v' )
                frontier.append(successor)
                #if(successor.id != curr.id):
                #    frontier.append(successor)
            elif d == 'left' and (empty_col_x-2) >= 0 and curr.board.grid[empty_col_y][empty_col_x-1] == '1': # there can be movemnent for piece '1' #8
                successor = create_a_successor(curr, empty_col_y, empty_col_x,(empty_col_y), (empty_col_x-2), 'left','1' )
                frontier.append(successor)
                #if(successor.id != curr.id):
                #    frontier.append(successor)
            elif d == 'right' and (empty_col_x+1) <= 3 and curr.board.grid[empty_col_y][empty_col_x+1] == '^': # there can be movemnent for piece 'v'
                successor = create_a_successor(curr, empty_col_y, empty_col_x,(empty_col_y), (empty_col_x+1), 'right','v' )
                frontier.append(successor)
                #if(successor.id != curr.id):
                #    frontier.append(successor)
            elif d == 'right' and (empty_col_x+2) <= 3 and curr.board.grid[empty_col_y][empty_col_x+1] == '1': # there can be movemnent for piece '1'
                successor = create_a_successor(curr, empty_col_y, empty_col_x,(empty_col_y), (empty_col_x+1), 'right','1' )
                frontier.append(successor)
                #if(successor.id != curr.id):
                #    frontier.append(successor)

    if ((first_empty[1]+1 == second_empty[1]) and (first_empty[0] == second_empty[0])) or ((first_empty[1]-1 == second_empty[1]) and (first_empty[0] == second_empty[0])): #horizontal empty row
        #do: create_a_successor for the vertial movement
        empty_col_y = first_empty[0]
        empty_col_x = min(first_empty[1], second_empty[1] )
        #print('first_empty x:'first_empty[1])
        #print('second_empty x:'second_empty[1])
        #print('empty_col_x = min :', empty_col_x)
        for d in direction:
            if d == 'up' and (empty_col_y-1) >= 0 and curr.board.grid[empty_col_y-1][empty_col_x] == '<': # there can be movemnent for piece 'v'
                successor = create_a_successor(curr, empty_col_y, empty_col_x,(empty_col_y-1), (empty_col_x), 'up','h' )
                frontier.append(successor)
                #if(successor.id != curr.id):
                #    frontier.append(successor)
            elif d == 'up' and (empty_col_y-2) >= 0 and curr.board.grid[empty_col_y-1][empty_col_x] == '1': # there can be movemnent for piece '1' #12 #bug detected
                successor = create_a_successor(curr, empty_col_y, empty_col_x,(empty_col_y-2), (empty_col_x), 'up','1' )
                frontier.append(successor)
                #if(successor.id != curr.id):
                #    frontier.append(successor)
                #print('first_empty x:',first_empty[1])
                #print('second_empty x:',second_empty[1])
                #print('empty_col_x = min :', empty_col_x)
            elif d == 'down' and (empty_col_y+1) <= 4 and curr.board.grid[empty_col_y+1][empty_col_x] == '<': # there can be movemnent for piece 'v'
                successor = create_a_successor(curr, empty_col_y, empty_col_x,(empty_col_y+1), (empty_col_x), 'down','h' )
                frontier.append(successor)
                #if(successor.id != curr.id):
                #    frontier.append(successor)
            elif d == 'down' and (empty_col_y+2) <= 4 and curr.board.grid[empty_col_y+1][empty_col_x] == '1': # there can be movemnent for piece '1'
                successor = create_a_successor(curr, empty_col_y, empty_col_x,(empty_col_y+1), (empty_col_x), 'down','1' )
                frontier.append(successor)
                #if(successor.id != curr.id):
                #    frontier.append(successor)
    #print("frontier has: ", len(frontier))
    
    

def dfs(board):
    
    frontier = []
    #explored = []
    #explored_ids = [] # give it a try to see if fix the problem
    explored_ids = set()
    init_state = State( board, 0, 0, None)
    frontier.append(init_state)
    #dfs_while_loop_couner = 0
    #count_for_break_while_loop = 0
    while(len(frontier)!= 0 ):
        
        #print("dfs_while_loop_couner: ", dfs_while_loop_couner)
        #dfs_while_loop_couner += 1
        #curr = frontier[-1] #curr is a state
        curr = frontier.pop()
        #print("a2")
        #helper function to check if curr is explored #bool def is_explored(curr, explored)
        #curr_is_explored = is_explored(curr, explored)
        #curr_id_is_explored = is_id_explored(curr.id, explored_ids )
        #print('curr_is_explored: ', curr_is_explored)
        #print('curr_id_is_explored: ', curr_id_is_explored)
        if not curr.id in explored_ids: #curr_is_explored
        #if curr_id_is_explored == False: #curr_is_explored
            #explored.append(curr)
            #explored_ids.append(curr.id)
            explored_ids.add(curr.id)
            print(curr.id)
            #need helper function to check if this board config is the same as goal board config, deep board compare
            #bool def is_at_goal(curr.board) implemented
            reached_goal = is_at_goal(curr)
            #print('reached_goal? :', reached_goal )
            if reached_goal == True:
                #print("b")
                return curr #curr contains the parent, so this helps us to trace the path, we will need to implement the adding parent featrue
            else:
                #print("c")
                #do: add curr's successors to Frontier #also put the parrent = curr for all the succesors
                #def add_curr_succ_to_frontier(curr, frontier)
                add_curr_succ_to_frontier(curr, frontier)
                #print('frontier[] now has: ', len(frontier))
        ''' 
        count_for_break_while_loop += 1
        if count_for_break_while_loop  <-70:
            print("forced break here:")
            print("length of explored: ", len(explored))
            test_pruning_write_to_text_dfs(explored)
            break
        '''

    #board.display()
    #return reach_goal
    
    '''
    #sudo code below for dfs:    
        #do: select and remore state curr from frontier
        curr = frontier[-1]
        frontier.pop()

        curr_explored = False
        for i in frontier:
            if i == curr: #exist //maybe need to use deepcopy to compare // eg: if i.board deep check equal to curr.board
                curr_explored = True

        #do: if curr is not explored:
        #if curr_explored == False:  
            #add curr to explored
            #if curr is a goal state:
                #return curr
            #else:
                #do: add curr's succeesors to frontier #do dfs here by adding up down left right with empty valid paths to the frontier..
                #helper_dfs_func()
        #else: //do nothing , it will start the while loop again
    '''
    
#def order_ini_to_goal(reach_goal):

def list_goal_to_init(reach_goal):
    list_to_write_on_txt = []
    current = reach_goal
    next = current.parent
    list_to_write_on_txt.append(current)
    while(next != None):
        current = current.parent
        list_to_write_on_txt.append(current)
        next = current.parent
    
    return list_to_write_on_txt

def write_to_text(reach_goal):
    list_to_write_on_txt = list_goal_to_init(reach_goal)
    f = open(output_file, "w")
    
    while(len(list_to_write_on_txt) != 0):
        last = list_to_write_on_txt[-1]
        count_y = 0
        for y in last.board.grid:
            #print(last.board.grid[count_y])
            f.writelines(last.board.grid[count_y])
            f.write("\n")
            count_y += 1
        f.write("\n")
        list_to_write_on_txt.pop()
    f.close()

def test_pruning_write_to_text_dfs(list_states):
    #list_to_write_on_txt = list_goal_to_init(reach_goal)
    f = open(output_file, "w")
    
    while(len(list_states) != 0):
        print(type(list_states[0]))
        first = list_states[0].board.grid
        count_y = 0
        for y in first:
            print(first[count_y])
            f.writelines(first[count_y])
            f.write("\n")
            count_y += 1
        f.write("\n")
        list_states.pop(0)
    f.close()

def write_a_grid_txt(grid):
    f = open(output_file, "w")
    count_y = 0
    for y in grid:
        print(grid[count_y])
        f.writelines(grid[count_y])
        f.write("\n")
        count_y += 1
    f.write("\n")
    f.close()
    '''    
    for each_config in list_to_write_on_txt:
        count_y = 0
        for y in each_config.board.grid:
            print(each_config.board.grid[count_y])
            f.writelines(each_config.board.grid[count_y])
            f.write("\n")
            count_y += 1
        f.write("\n")
    f.close()
    '''
#-------------------------------------------Below is astar----------------------------------------------
def manhattan_h(curr_goal_x, curr_goal_y):
    goal_x = 1  
    goal_y = 3
    x_d = abs(goal_x - curr_goal_x)
    y_d = abs(goal_y - curr_goal_y)
    h = x_d + y_d
    return h


def create_a_successor_astar(curr, empty_y, empty_x, piece_y, piece_x, d, shape ):
    curr_f = curr.f
    curr_depth = curr.depth
    deepcopied_pieces = deepcopy(curr.board.pieces)
    
    for p in deepcopied_pieces:
        if (d=='up' or d=='down' or d=='left' or d=='right') and shape=='2' and p.is_single==True and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
        elif d=='up' and shape=='v'and p.orientation=='v' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y - 1
            p.coord_x = empty_x
        elif d=='down' and shape=='v' and p.orientation=='v' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
        elif d=='left' and shape=='h' and p.orientation=='h' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x - 1
        elif d=='right' and shape=='h' and p.orientation=='h' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
        elif (d=='left' or d=='right') and shape=='v' and p.orientation=='v' and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
        elif d=='left' and shape=='1' and p.is_goal==True and p.coord_y==piece_y and p.coord_x==piece_x: #8
            p.coord_y = empty_y
            p.coord_x = empty_x-1
        elif d=='right' and shape=='1' and p.is_goal==True and p.coord_y==piece_y and p.coord_x==piece_x:
            p.coord_y = empty_y
            p.coord_x = empty_x
        elif (d=='up' or d=='down') and shape=='h' and p.orientation=='h' and p.coord_y==piece_y and p.coord_x==piece_x: #11 and #14
            p.coord_y = empty_y
            p.coord_x = empty_x
        elif d=='up' and shape=='1' and p.is_goal==True and p.coord_y==piece_y and p.coord_x==piece_x: #12
            p.coord_y = empty_y-1
            p.coord_x = empty_x
        elif d=='down' and shape=='1' and p.is_goal==True and p.coord_y==piece_y and p.coord_x==piece_x: #13
            p.coord_y = empty_y
            p.coord_x = empty_x 

    new_identical_board = Board(deepcopied_pieces)
    #board, f, depth, parent=None 
    curr_goal_x = None
    curr_goal_y = None
    for p in new_identical_board.pieces:
        if p.is_goal == True:
            curr_goal_x = p.coord_x
            curr_goal_y = p.coord_y

    h_for_this_succ = manhattan_h(curr_goal_x, curr_goal_y)
    successor = State( new_identical_board, (h_for_this_succ + curr_depth + 1), curr_depth+1, curr)
    #successor.board.grid = []
    #successor.board._Board__construct_grid()
    #successor.board.display()
    successor.id = hash_board_config(successor.board) 
    return successor


def add_curr_succ_to_frontier_astar(curr, frontier):
    direction = ['up', 'down', 'left', 'right']
    empty_squares = []
    y_coord = 0
    #print('add_curr_succ_to_frontier')
    for y in curr.board.grid: #start with y-axis
        x_coord = 0
        #debuging: print("y loop:" + str(y_coord))
        for x in y: #then x-axis
            if x == '.':
                empty_squares.append([y_coord, x_coord]) #will be used for cheking if two . are next to each other
                for d in direction:
                    if d == 'up' and (y_coord-1) >= 0 and curr.board.grid[y_coord-1][x_coord] == '2': # there can be movemnent for piece '2'
                        successor = create_a_successor_astar(curr, y_coord, x_coord,(y_coord-1),x_coord, 'up', '2' )
                        #frontier.append(successor)
                        heappush(frontier, (successor.f, successor))
                    elif d == 'up' and (y_coord-2) >= 0 and curr.board.grid[y_coord-1][x_coord] == 'v': # there can be movemnent for piece 'v'
                        successor = create_a_successor_astar(curr, y_coord, x_coord,(y_coord-2),x_coord, 'up','v' )
                        #frontier.append(successor)
                        heappush(frontier, (successor.f, successor))
                    elif d == 'down' and (y_coord+1) <= 4 and curr.board.grid[y_coord+1][x_coord] == '2': # there can be movemnent for piece '2'
                        successor = create_a_successor_astar(curr, y_coord, x_coord,(y_coord+1),x_coord, 'down', '2' ) #this line cuz rasing errors!!!
                        #frontier.append(successor)
                        heappush(frontier, (successor.f, successor))
                    elif d == 'down' and (y_coord+2) <= 4 and curr.board.grid[y_coord+1][x_coord] == '^': # there can be movemnent for piece 'v'
                        successor = create_a_successor_astar(curr, y_coord, x_coord,(y_coord+1),x_coord, 'down','v' )
                        #frontier.append(successor)
                        heappush(frontier, (successor.f, successor))
                    elif d == 'left' and (x_coord-1) >= 0 and curr.board.grid[y_coord][x_coord-1] == '2': # there can be movemnent for piece '2'
                        successor = create_a_successor_astar(curr, y_coord, x_coord,y_coord, (x_coord-1), 'left', '2' )
                        #frontier.append(successor)
                        heappush(frontier, (successor.f, successor))
                    elif d == 'left' and (x_coord-2) >= 0 and curr.board.grid[y_coord][x_coord-1] == '>': # there can be movemnent for piece 'v'
                        successor = create_a_successor_astar(curr, y_coord, x_coord,(y_coord), (x_coord-2), 'left','h' )
                        #frontier.append(successor)
                        heappush(frontier, (successor.f, successor))
                    elif d == 'right' and (x_coord+1) <= 3 and curr.board.grid[y_coord][x_coord+1] == '2': # there can be movemnent for piece '2'
                        successor = create_a_successor_astar(curr, y_coord, x_coord,y_coord, (x_coord+1), 'right', '2' )
                        #frontier.append(successor)
                        heappush(frontier, (successor.f, successor))
                    elif d == 'right' and (x_coord+2) <= 3 and curr.board.grid[y_coord][x_coord+1] == '<': # there can be movemnent for piece 'v'
                        successor = create_a_successor_astar(curr, y_coord, x_coord,y_coord, (x_coord+1), 'right','h' )
                        #frontier.append(successor)
                        heappush(frontier, (successor.f, successor))
            x_coord += 1    
        y_coord += 1
    #now need to check if the two empty square is next to each other
    first_empty = empty_squares[0]
    second_empty = empty_squares[1]
    #first_empty[0] is y coordinate, first_empty[1] is x coordinate
    if ((first_empty[0]+1 == second_empty[0]) and (first_empty[1] == second_empty[1])) or ((first_empty[0]-1 == second_empty[0]) and (first_empty[1] == second_empty[1])): #vertical empty column
        #do: create_a_successor for the horizontal movement
        empty_col_y = min(first_empty[0], second_empty[0])
        empty_col_x = first_empty[1]
        for d in direction:
            if d == 'left' and (empty_col_x-1) >= 0 and curr.board.grid[empty_col_y][empty_col_x-1] == '^': # there can be movemnent for piece 'v'
                successor = create_a_successor_astar(curr, empty_col_y, empty_col_x,(empty_col_y), (empty_col_x-1), 'left','v' )
                #frontier.append(successor)
                heappush(frontier, (successor.f, successor))
            elif d == 'left' and (empty_col_x-2) >= 0 and curr.board.grid[empty_col_y][empty_col_x-1] == '1': # there can be movemnent for piece '1' #8
                successor = create_a_successor_astar(curr, empty_col_y, empty_col_x,(empty_col_y), (empty_col_x-2), 'left','1' )
                #frontier.append(successor)
                heappush(frontier, (successor.f, successor))
            elif d == 'right' and (empty_col_x+1) <= 3 and curr.board.grid[empty_col_y][empty_col_x+1] == '^': # there can be movemnent for piece 'v'
                successor = create_a_successor_astar(curr, empty_col_y, empty_col_x,(empty_col_y), (empty_col_x+1), 'right','v' )
                #frontier.append(successor)
                heappush(frontier, (successor.f, successor))
            elif d == 'right' and (empty_col_x+2) <= 3 and curr.board.grid[empty_col_y][empty_col_x+1] == '1': # there can be movemnent for piece '1'
                successor = create_a_successor_astar(curr, empty_col_y, empty_col_x,(empty_col_y), (empty_col_x+1), 'right','1' )
                #frontier.append(successor)
                heappush(frontier, (successor.f, successor))

    if ((first_empty[1]+1 == second_empty[1]) and (first_empty[0] == second_empty[0])) or ((first_empty[1]-1 == second_empty[1]) and (first_empty[0] == second_empty[0])): #horizontal empty row
        #do: create_a_successor for the vertial movement
        empty_col_y = first_empty[0]
        empty_col_x = min(first_empty[1], second_empty[1] )
        for d in direction:
            if d == 'up' and (empty_col_y-1) >= 0 and curr.board.grid[empty_col_y-1][empty_col_x] == '<': # there can be movemnent for piece 'v'
                successor = create_a_successor_astar(curr, empty_col_y, empty_col_x,(empty_col_y-1), (empty_col_x), 'up','h' )
                #frontier.append(successor)
                heappush(frontier, (successor.f, successor))
            elif d == 'up' and (empty_col_y-2) >= 0 and curr.board.grid[empty_col_y-1][empty_col_x] == '1': # there can be movemnent for piece '1' #12 #bug detected
                successor = create_a_successor_astar(curr, empty_col_y, empty_col_x,(empty_col_y-2), (empty_col_x), 'up','1' )
                #frontier.append(successor)
                heappush(frontier, (successor.f, successor))
            elif d == 'down' and (empty_col_y+1) <= 4 and curr.board.grid[empty_col_y+1][empty_col_x] == '<': # there can be movemnent for piece 'v'
                successor = create_a_successor_astar(curr, empty_col_y, empty_col_x,(empty_col_y+1), (empty_col_x), 'down','h' )
                #frontier.append(successor)
                heappush(frontier, (successor.f, successor))
            elif d == 'down' and (empty_col_y+2) <= 4 and curr.board.grid[empty_col_y+1][empty_col_x] == '1': # there can be movemnent for piece '1'
                successor = create_a_successor_astar(curr, empty_col_y, empty_col_x,(empty_col_y+1), (empty_col_x), 'down','1' )
                #frontier.append(successor)
                heappush(frontier, (successor.f, successor))

def find_lowest_f(frontier):
    fron_w_lowest_f = frontier[0]
    ind_w_lowest_f = 0
    for index, element in enumerate(frontier):
        if element.f < fron_w_lowest_f.f:
            fron_w_lowest_f = element
            ind_w_lowest_f = index
    return ind_w_lowest_f

def astar(board):
    frontier = []
    explored_ids = set()
    init_state = State( board, 0, 0, None)
    #frontier.append(init_state)
    heappush(frontier, (init_state.f, init_state))
    while(len(frontier)!= 0 ):
        #do: helper function that finds the smallest f value
        #ind_w_lowest_f = find_lowest_f(frontier)
        #curr = frontier.pop(ind_w_lowest_f)
        curr_tuple = heappop(frontier)
        curr = curr_tuple[1]
        if not curr.id in explored_ids: #curr_is_explored
            explored_ids.add(curr.id)
            print(curr.id)
            reached_goal = is_at_goal(curr)
            if reached_goal == True:
                return curr #curr contains the parent, so this helps us to trace the path, we will need to implement the adding parent featrue
            else:
                add_curr_succ_to_frontier_astar(curr, frontier)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    parser.add_argument(
        "--algo",
        type=str,
        required=True,
        choices=['astar', 'dfs'],
        help="The searching algorithm."
    )
    args = parser.parse_args()

    # read the board from the file
    board = read_from_file(args.inputfile)
    

    #print(sys.getrecursionlimit())
    #sys.setrecursionlimit(2000)
    output_file = args.outputfile
    #print('below is user expected output file:')
    #print(output_file)
    #print(board.grid)
    '''Glen's code below:
    print(hash_board_config(board))
    print(hash_board_config(board))

    print(board.grid)
    
    s = str(board.grid)
    print(s)
    print(type(s))
    #print('\n')
    a = hash(s)
    print(a)
    
    print('\n now it is b time: ')
    print(board.grid)
    print(str(board.grid))
    b = hash(str(board.grid))
    print(b)
    '''

 
    if args.algo == 'dfs':
        reach_goal = dfs(board)
        #test this by see if reach_goal is at goal state
        #print(reach_goal)
        #reach_goal.board.display()
        write_to_text(reach_goal)

        #start_to_goal = order_ini_to_goal(reach_goal) # this function reversed the order of this reach_goal linked list

        #do: helpfer function to generate path from inital to goal
        #order_ini_to_goal(reach_goal)
        #do: helper function to write this order_ini_to_goal into txt
        #write_path_to_output_txt

    elif args.algo == 'astar':
        reach_goal = astar(board)
        write_to_text(reach_goal)
        print("count: ", reach_goal.depth)
    
    
    




'''
def create_a_successor_for_2(curr, empty_y, empty_x, y_for_2, x_for_2):
    successor = deepcopy(curr)
    #both pieces and grid are needed to be edited, but grid can be edited by calling _contruct_grid
    #edit the pieces
    for p in successor.board.pieces:
        if p.is_single == True and p.coord_y == y_for_2 and p.coord_x == x_for_2:
            p.coord_y = empty_y
            p.coord_x = empty_x
    successor.board.grid = []
    successor.board.__construct_grid()
    return successor

def create_a_successor_for_move_up_v(curr, empty_y, empty_x, y_for_v, x_for_v):
    successor = deepcopy(curr)
    #both pieces and grid are needed to be edited, but grid can be edited by calling _contruct_grid
    #edit the pieces
    for p in successor.board.pieces:
        if p.orientation == 'v' and p.coord_y == y_for_v and p.coord_x == x_for_v:
            p.coord_y = empty_y - 1
            p.coord_x = empty_x
    successor.board.grid = []
    successor.board.__construct_grid()
    return successor
'''