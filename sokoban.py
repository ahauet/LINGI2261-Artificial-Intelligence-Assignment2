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






def isGoalPoint(point, goalPoints):
    for p in goalPoints:
        if p[0] == point[0] and p[1] == point[1]:
            return True
    return False


class Sokoban(Problem):

    def __init__(self, grid, smiley, boxesPostions, goalPoints):
        self.nbrExploredNodes = 0
        self.grid = grid
        self.goalPoints = goalPoints
        self.initState = State(smiley, boxesPostions)
        self.goalState = State(None, goalPoints)

        super().__init__(self.initState, self.goalState)

    def successor(self, state):
        # dicoDirections = heuristic(state, goalPoints) #heuristic will return a dictionnary that associate each direction to a value. ex: {'L' : 1, 'R': 8, 'U': 9, 'D': 4}
        # dicoDirections.sort(orderHeuristic)
        for direction in directions.values():
            newState = self.authorizedMov(state, direction, self.goalPoints) #authorizedMov return a newState if the mvoement is valid, else return NONE
            if newState: #movement authorized
                if not self.deadState(state, newState, direction):#ok
                    self.nbrExploredNodes += 1
                    #print(newState)
                    yield (direction, newState)

    def authorizedMov(self, state , direction, goalPoints):
        x = state.smileyPosition[0]+direction[0]
        y = state.smileyPosition[1]+direction[1]
        if self.getGridContentAtPos(state, (x,y)) != '#':
            newBoxesPoint = copy.deepcopy(state.boxesPositions)
            if self.getGridContentAtPos(state, (x,y)) == '$':
                #if isGoalPoint([x, y], goalPoints):
                #    return None
                xBox = x + direction[0]
                yBox = y + direction[1]
                if self.getGridContentAtPos(state, (xBox,yBox)) == '$' or self.getGridContentAtPos(state, (xBox,yBox)) == '#':
                    return None
                newBoxesPoint = updateBoxesPoint(state.boxesPositions, (x,y), (xBox,yBox))
            return State((x,y), newBoxesPoint)
        return  None

    def getGridContentAtPos(self, state, position):
        """
        Look in the grid for the content of pos
        Warning, pos must be in the bounds of the grid
        :param pos: (x,y)
        :return: grid[x][y]
        """
        if self.grid[position[0]][position[1]] == '#':
            return '#'
        if position[0] == state.smileyPosition[0] and position[1] == state.smileyPosition[1]:
            return '@'
        for boxe in state.boxesPositions:
            if position[0] == boxe[0] and position[1] == boxe[1]:
                return '$'
        return ' '

    def deadState(self, previousState, state, direction):
        """Check if the smiley had pushed a box
        If yes, check if there is a dead state with this box
        Else, return false

        :param previousGrid: matrix representing the grid before smiley moved
        :param grid: matrix representing the grid after the smiley moved
        :param smileyPos: (x,y) coordinates of the smiley after move
        :param direction: (a,b) direction in which the smiley moved
        :return: True if there is a dead state and False otherwise
        """
        if state.smileyPosition in previousState.boxesPositions : #we pushed a box
            pushedBoxPos = applyMove(state.smileyPosition, direction)
            if isGoalPoint(pushedBoxPos, self.goalPoints):
                return False
            else:
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
                upPos = applyMove(pushedBoxPos, directions['U'])
                if inBounds(self.grid, upPos):
                    if self.getGridContentAtPos(state, upPos) == '#':
                        leftPos = applyMove(pushedBoxPos, directions['L'])
                        if inBounds(self.grid, leftPos):
                            if self.getGridContentAtPos(state, leftPos) == '#':
                                return True
                        rightPos = applyMove(pushedBoxPos, directions['R'])
                        if inBounds(self.grid, rightPos):
                            if self.getGridContentAtPos(state, rightPos) == '#':
                                return True
                # Check if there is a wall down and left
                # Check if there is a wall down and right
                downPos = applyMove(pushedBoxPos, directions['D'])
                if inBounds(self.grid, downPos):
                    if self.getGridContentAtPos(state, downPos) == '#':
                        leftPos = applyMove(pushedBoxPos, directions['L'])
                        if inBounds(self.grid, leftPos):
                            if self.getGridContentAtPos(state, leftPos) == '#':
                                return True
                        rightPos = applyMove(pushedBoxPos, directions['R'])
                        if inBounds(self.grid, rightPos):
                            if self.getGridContentAtPos(state, rightPos) == '#':
                                return True

                # possible dead state 2)  ############   ############  ############   ############
                #                         #    $$    #   #          #  #          #   #          #
                #                         #          #   #  #$      #  #    $$    #   #    $#    #
                #                         #          #   #  #$      #  #    $$    #   #    $$    #
                #                         #          #   #          #  #          #   #          #
                #                         ############   ############  ############   ############

                #Check if there is a 2*2 square with no blank
                # subSquare1 = ([0, -1], [-1, 0], [-1, -1])  # Left, Down, Both
                # subSquare2 = ([0, 1], [-1, 0], [-1, 1])  # Right, Down, Both
                # subSquare3 = ([0, -1], [1, 0], [1, -1])  # Left, Up, Both
                # subSquare4 = ([0, 1], [1, 0], [1, 1])  # Right, Up, Both
                # subSquares = [subSquare1, subSquare2, subSquare3, subSquare4]
                #
                # for subSquare in subSquares:
                #     hasBlank = False
                #     for direction in subSquare:
                #         pos = applyMove(pushedBoxPos, direction)
                #         if inBounds(self.grid, pos):
                #             if self.getGridContentAtPos(state, pos) == ' ':
                #                 hasBlank = True
                #                 break #the square hasn't 4 full blocks
                #     if not hasBlank:
                #         return True

        return False #we didn't pushed a box or there is no dead states

    def heuristic(self, node):
        boxPoints = node.state.boxesPositions
        smileyPos = node.state.smileyPosition
        sum = 0
        shorterSmi = 9223372036854775807
        for box in boxPoints:
            manhattan1 = abs(smileyPos[0]-box[0]) + abs(smileyPos[1]-box[1])
            if manhattan1 < shorterSmi:
                shorterSmi = manhattan1
            shorterBox = 9223372036854775807
            for goal in self.goalPoints:
                manhattan2 = abs(goal[0]-box[0]) + abs(goal[1]-box[1])
                if manhattan2 < shorterBox :
                    shorterBox = manhattan2
            sum += manhattan2
        sum += shorterSmi
        return sum


class State:

    def __init__(self, smileyPosition, boxesPositions):
        self.smileyPosition = smileyPosition
        self.boxesPositions = boxesPositions



    def __eq__(self, other):
        for box in self.boxesPositions:
            if not box in other.boxesPositions:
                return False
        return True

    def __hash__(self):
        # hashvalue = 0
        # for i in range(0, len(self.grid)):
        #     for j in range(0, len(self.grid[0])):
        #         x = grid[i][j]
        #         hashvalue +=
        return hash(str(self))


    def __str__(self):
        output = ""
        for i in range(0, len(problem.grid)):
            for j in range(0, len(problem.grid[0])):
                output += problem.getGridContentAtPos(self, (i,j))
            output += '\n'
        return output



def inBounds(grid, pos):
    """Check if a position is inside the bounds of a grid"""
    return 0 <= pos[0] and pos[0] < len(grid) and 0 <= pos[1] and pos[1] < len(grid[0])

def constructGrid(problemFileName):
    """
    Open and interpret a file as a grid
    :rtype : a matrix representing the problem's grid
    """
    grid = []
    smiley = None
    boxes = []
    try:
        file = open(problemFileName + ".init")
        i = 0
        for line in file.readlines():
            j = 0
            tmp = []
            for character in line:
                if character != '\n':
                    if character == '@':
                        smiley = (i,j)
                        character = ' '
                    elif character == '$':
                        boxes.append((i,j))
                        character = ' '
                    tmp.append(character)
                j += 1
            grid.append(tmp)
            i += 1
    except IOError:
        print("File " + problemFileName + " can not be found or open")
        exit(1)
    else:
        return (grid, smiley, boxes)


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


def updateBoxesPoint(list, oldPosition, newPosition):
    resultList = copy.deepcopy(list)
    for i in range(0,len(resultList)) :
        if resultList[i][0] == oldPosition[0] and resultList[i][1] == oldPosition[1]:
            del resultList[i]
            resultList.append(newPosition)
            return resultList
    return None


def abs(n):
    return (n, -n)[n < 0]



#####################
# Launch the search #
#####################

start_time = time.time()

if len(sys.argv) < 2:
    print("usage: sokoban.py instance")
    exit(2)
tuple = constructGrid(sys.argv[1])
goalPoints = getGoalPoint(sys.argv[1])

problem = Sokoban(tuple[0], tuple[1], tuple[2], goalPoints)

# example of bfs search
node = astar_graph_search(problem, problem.heuristic)
# example of print
path = node.path()
path.reverse()
for n in path:
    print(n.state)  # assuming that the __str__ function of states output the correct format


print("--- %s seconds ---" % (time.time() - start_time))
print("--- %s nodes explored ---" % problem.nbrExploredNodes)
print("--- %s steps from root to solution ---" % (len(path) -1) )
