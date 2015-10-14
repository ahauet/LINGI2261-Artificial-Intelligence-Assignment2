'''NAMES OF THE AUTHOR(S): Alexandre Hauet & Tanguy Vaessen'''
import time
from search import *
import copy


def constructGoalGrid(grid, goalPoints):
    goalGrid = copy.deepcopy(grid)
    for point in goalPoints:
        goalGrid[point[0]][point[1]] = '$'
    return goalGrid

directions = {"L" : [0, -1], "R":[0, 1], "U":[1, 0], "D":[-1, 0]}  # Left, Right, Up, Down

def orderHeuristic(x,y):
    if (x[1] < y[1]):
        return -1
    elif(x[1] == y[1]):
        return 0
    else: return 1


def deadState(previousGrid, grid, previousPosition, direction):
    """Check if the smiley had push a box
    If yes, check if there is a dead state with this box
    Else, return false"""
    if previousGrid[previousPosition[0]][previousPosition[1]] != '$': #we pushed a box
        pass
    else:
        return False


def heuristic(state):
    print(state.grid)
    return True


def authorizedMov(grid, position, direction):
    return  True

class Sokoban(Problem):

    def __init__(self, grid, goalPoints):
        self.goalPoints = goalPoints
        self.initState = State(grid)
        self.goalState = State(constructGoalGrid(grid, goalPoints))

        super().__init__(self.initState, self.goalState)

    def successor(self, state):
        dicoDirections = heuristic(state) #heuristic will return a dictionnary that associate each direction to a value. ex: {'L' : 1, 'R': 8, 'U': 9, 'D': 4}
        dicoDirections.sort(orderHeuristic)
        for direction in dicoDirections:
            newState = authorizedMov(state.grid, state.smileyPosition, direction) #authorizedMov return a newState if the mvoement is valid, else return NONE
            if newState: #movement authorized
                if deadState(state.grid, newState.grid, state.smileyPosition, direction):#dead state
                    pass
                else: #ok
                    yield (direction, newState)
            else: #movement invalid : obstacle, ...
                pass


class State:

    def __init__(self, grid, pos):
        self.grid = grid
        self.smileyPosition = pos

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





#####################
# Launch the search #
#####################

start_time = time.time()

if len(sys.argv) < 2: print("usage: numberlink.py inputFile"); exit(2)
grid = constructGrid(sys.argv[1])
goalPoints = getGoalPoint(sys.argv[1])
smileyPos = getSmileyPos(grid)
print(grid)
print(goalPoints)
print(smileyPos)

problem = Sokoban(grid, goalPoints)
print(problem.goalState == problem.goalState)

exit(0)

# print(problem.initial.letter)
# print(problem.initial.position)
# for pair in problem.successor(problem.initial):
#    print(pair[0], pair[1].grid)
# exit(0)


print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s nodes explored ---" % problem.nbrExploredNodes)
#print("--- %s steps from root to solution ---" % (len(path) -1) )