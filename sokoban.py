'''NAMES OF THE AUTHOR(S): Alexandre Hauet & Tanguy Vaessen'''
import time
from search import *
import copy


def constructGoalGrid(grid, goalPoints):
    goalGrid = copy.deepcopy(grid)
    for point in goalPoints:
        goalGrid[point[0]][point[1]] = '$'
    return goalGrid


class Sokoban(Problem):

    def __init__(self, grid, goalPoints):
        self.goalPoints = goalPoints
        self.initState = State(grid)
        self.goalState = State(constructGoalGrid(grid, goalPoints))

        super().__init__(self.initState, self.goalState)



class State:

    def __init__(self, grid):
        self.grid = grid

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





#####################
# Launch the search #
#####################

start_time = time.time()

if len(sys.argv) < 2: print("usage: numberlink.py inputFile"); exit(2)
grid = constructGrid(sys.argv[1])
goalPoints = getGoalPoint(sys.argv[1])
print(grid)
print(goalPoints)

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
print("--- %s steps from root to solution ---" % (len(path) -1) )