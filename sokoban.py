"""NAMES OF THE AUTHOR(S): Alexandre Hauet & Tanguy Vaessen"""
import time
from search import *
import copy


def constructGoalGrid(grid, goalPoints):
    """
    Add the goal point to a copy of the grid
    :param grid: matrix
    :param goalPoints: list
    :return: matrix
    """
    goalGrid = copy.deepcopy(grid)
    for point in goalPoints:
        goalGrid[point[0]][point[1]] = '$'
    return goalGrid

directions = {"L" : [0, -1], "R":[0, 1], "U":[-1, 0], "D":[1, 0]}  # Left, Right, Up, Down

def orderHeuristic(x,y):
    """
    Compare two integers
    :param x:
    :param y:
    :return: 0 if equals, -1 if x < y, 1 if x >= y
    """
    if x[1] < y[1]:
        return -1
    elif x[1] == y[1]:
        return 0
    else: return 1


def applyMove(point, direction):
    """
    apply the move direction to point
    :param point: (x,y)
    :param direction: (a,b)
    :return: (x+a, y+b)
    """
    return [
        point[0] + direction[0],
        point[1] + direction[1]
    ]


def getGridContentAtPos(grid, pos):
    """
    Look in the grid for the content of pos
    Warning, pos must be in the bounds of the grid
    :param pos: (x,y)
    :return: grid[x][y]
    """
    return grid[pos[0]][pos[1]]

def deadState(previousGrid, grid, smileyPos, direction):
    """Check if the smiley had push a box
    If yes, check if there is a dead state with this box
    Else, return false

    :param previousGrid: matrix representing the grid before smiley moved
    :param grid: matrix representing the grid after the smiley moved
    :param smileyPos: (x,y) coordinates of the smiley after move
    :param direction: (a,b) direction in which the smiley moved
    :return: True if there is a dead state and False otherwise
    """
    if previousGrid[smileyPos[0]][smileyPos[1]] == '$': #we pushed a box
        pushedBoxPos = applyMove(smileyPos, direction)

        # we need to check if there is a dead state with the box we pushed
        #
        # possible dead state 1)  ############   ############
        #                         #$         #   #          #
        #                         #          #   #    #     #
        #                         #          #   #   #$     #
        #                         #          #   #          #
        #                         ############   ############
        #

        #Check if there is a wall up and left
        #Check if there is a wall up and right
        upPos = applyMove(pushedBoxPos, direction['U'])
        if inBounds(grid, upPos):
            if getGridContentAtPos(grid, upPos) == '#':
                leftPos = applyMove(pushedBoxPos, direction['L'])
                if inBounds(grid, leftPos):
                    if getGridContentAtPos(grid, leftPos) == '#':
                        return True
                rightPos = applyMove(pushedBoxPos, direction['R'])
                if inBounds(grid, rightPos):
                    if getGridContentAtPos(grid, rightPos) == '#':
                        return True
        # Check if there is a wall down and left
        # Check if there is a wall down and right
        downPos = applyMove(pushedBoxPos, direction['D'])
        if inBounds(grid, downPos):
            if getGridContentAtPos(grid, downPos) == '#':
                leftPos = applyMove(pushedBoxPos, direction['L'])
                if inBounds(grid, leftPos):
                    if getGridContentAtPos(grid, leftPos) == '#':
                        return True
                rightPos = applyMove(pushedBoxPos, direction['R'])
                if inBounds(grid, rightPos):
                    if getGridContentAtPos(grid, rightPos) == '#':
                        return True

        # possible dead state 2)  ############   ############  ############   ############
        #                         #    $$    #   #          #  #          #   #          #
        #                         #          #   #  #$      #  #    $$    #   #    $#    #
        #                         #          #   #  #$      #  #    $$    #   #    $$    #
        #                         #          #   #          #  #          #   #          #
        #                         ############   ############  ############   ############

        #Check if there is a 2*2 squarre with no blank
        subSquarre1 = ([0, -1], [-1, 0], [-1, -1])  # Left, Down, Both
        subSquarre2 = ([0, 1], [-1, 0], [-1, 1])  # Right, Down, Both
        subSquarre3 = ([0, -1], [1, 0], [1, -1])  # Left, Up, Both
        subSquarre4 = ([0, 1], [1, 0], [1, 1])  # Right, Up, Both
        subSquarres = [subSquarre1, subSquarre2, subSquarre3, subSquarre4]

        for subSquarre in subSquarres:
            hasBlank = False
            for direction in subSquarre:
                pos = applyMove(pushedBoxPos, direction)
                if inBounds(grid, pos):
                    if getGridContentAtPos(grid, pos) == ' ':
                        hasBlank = True
                        break #the square hasn't 4 full blocks
            if not hasBlank:
                return True

    return False #we didn't pushed a box or there is no dead states


def heuristic(node):
    result = {}
    boxPoints = getBoxesPoint(node.state.grid)
    smileyPos = getSmileyPos(node.state.grid)
    sum = 0
    shorterSmi = 9223372036854775807
    if grid[node.state.smileyPosition[0]][node.state.smileyPosition[1]] != '#':
        for box in boxPoints:
            manhattan1 = abs(smileyPos[0]-box[0]) + abs(smileyPos[1]-box[1])
            if manhattan1 < shorterSmi:
                shorterSmi = manhattan1
            shorterBox = 9223372036854775807
            for goal in node.state.goalPoints:
                manhattan2 = abs(goal[0]-box[0]) + abs(goal[1]-box[1])
                if manhattan2 < shorterBox :
                    shorterBox = manhattan2
            sum += manhattan2
        sum += shorterSmi
    return sum


def authorizedMov(grid, position, direction):
    return  True

class Sokoban(Problem):

    def __init__(self, grid, goalPoints):
        self.goalPoints = goalPoints
        self.initState = State(grid, getSmileyPos(grid), goalPoints)
        self.goalState = State(constructGoalGrid(grid, goalPoints), None, None)

        super().__init__(self.initState, self.goalState)

    def successor(self, state):
        # dicoDirections = heuristic(state, goalPoints) #heuristic will return a dictionnary that associate each direction to a value. ex: {'L' : 1, 'R': 8, 'U': 9, 'D': 4}
        # dicoDirections.sort(orderHeuristic)
        for direction in directions.values():
            newState = authorizedMov(state.grid, state.smileyPosition, direction) #authorizedMov return a newState if the mvoement is valid, else return NONE
            if newState: #movement authorized
                if deadState(state.grid, newState.grid, newState.smileyPosition, direction):#dead state
                    pass
                else: #ok
                    yield (direction, newState)
            else: #movement invalid : obstacle, ...
                pass


class State:

    def __init__(self, grid, pos, goalPoints):
        self.grid = grid
        self.smileyPosition = pos
        self.goalPoints = goalPoints

    def __eq__(self, other):
        for i in range(0, len(self.grid)):
            for j in range(0, len(self.grid[0])):
                if self.grid[i][j] != other.grid[i][j]:
                    return False
        return True



def inBounds(grid, pos):
    """Check if a position is inside the bounds of a grid"""
    return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])

def constructGrid(problemFileName):
    """
    Open and interpret a file as a grid
    :rtype : a matrix representing the problem's grid
    """
    grid = []
    try:
        file = open(problemFileName + ".init")
        for line in file.readlines():
            tmp = []
            for character in line:
                if character != '\n':
                    tmp.append(character)
            grid.append(tmp)
    except IOError:
        print("File " + problemFileName + " can not be found or open")
        exit(1)
    else:
        return grid


def getGoalPoint(fileName):
    """Open an interpret a goal file
    Return a list of position (x,y)
    Each point is a goal point"""
    result=[]
    x=0
    y=0
    try:
        file = open(fileName + ".goal")
        for line in file.readlines():
            for character in line:
                if character == '.':
                    result.append((x,y))
                y+=1
            x+=1
            y=0
    except IOError:
        print("File " + fileName + " can not be found or open")
        exit(1)
    return result

def getBoxesPoint(grid):
    result=[]
    x=0
    y=0
    while x < len(grid):
        while y < len(grid[x]):
            if grid[x][y] == '$':
                result.append((x,y))
            y+=1
        x+=1
        y=0
    return result

def getSmileyPos(grid):
    result=[]
    x=0
    y=0
    while x < len(grid):
        while y < len(grid[x]):
            if grid[x][y] == '@':
                return (x,y)
            y+=1
        x+=1
        y=0
    return None

def abs(n):
    return (n, -n)[n < 0]



#####################
# Launch the search #
#####################

start_time = time.time()

if len(sys.argv) < 2:
    print("usage: numberlink.py inputFile")
    exit(2)
grid = constructGrid(sys.argv[1])
goalPoints = getGoalPoint(sys.argv[1])
smileyPos = getSmileyPos(grid)

problem = Sokoban(grid, goalPoints)

# example of bfs search
node = astar_graph_search(problem, heuristic)
# example of print
path = node.path()
path.reverse()
for n in path:
    print(n.state)  # assuming that the __str__ function of states output the correct format


print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s nodes explored ---" % problem.nbrExploredNodes)
print("--- %s steps from root to solution ---" % (len(path) -1) )
