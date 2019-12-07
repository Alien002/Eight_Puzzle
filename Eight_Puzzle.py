import os
import random
import copy
import heapq as priQ
import numpy as np


#Node stores Array, and uniform, heuristic, and cost values.
class node:
    def __init__(self, data = None):
        self.data = data
        self.uniform = 0
        self.heuristic = 0
        self.cost = 1
    
    #needed to accomodate heapq
    def __lt__(self, other):
        return self.cost < other.cost

    def __le__(self,other):
        return self.cost <= other.cost

    def __gt__(self, other):
        return self.cost > other.cost

    def __ge__(self, other):
        return self.cost >= other.cost
        
    #Checks to see if current node is solved (based on Goal Node)
    def solved(self):
        for i in range(3):
            for j in range(3):
                if(self.data[i][j] != GOAL[i][j]):
                    return False
        return True
        
    #Checks if current node is repeated (compares with boards in the visited array)
    def isRepeat(self, dir_node):
        c = 0
        matched = 0
        temp_matched = 0
        while c < len(dir_node):
            check_node = dir_node[c]
            temp_matched = 0
            for i in range(3):
                for j in range(3):
                    if self.data[i][j] == check_node.data[i][j]:
                        temp_matched += 1
            matched = max(matched, temp_matched)
            c += 1
        if matched == 9:
            return True
        return False

        
##

#Initial Blank Puzzle
INIT = np.array([[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]])
#Default Puzzle Can Change
DEFAULT = np.array([[1, 2, 3],
                    [4, 8, 0],
                    [7, 6, 5]])
   
##Assigned Test Cases##

#Trivial
TRIVIAL = np.array([[1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 0]])

#Very Easy
VEASY = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 0, 8]])
       
#Easy
EASY = np.array([[1, 2, 0],
                 [4, 5, 3],
                 [7, 8, 6]])
#Doable
DOABLE = np.array([[0, 1, 2],
                   [4, 5, 3],
                   [7, 8, 6]])
#Oh Boy
OHBOY = np.array([[8, 7, 1],
                  [6, 0, 2],
                  [5, 4, 3]])

#Impossible
IMPOSSIBLE = np.array([[1, 2, 3],
                       [4, 5, 6],
                       [8, 7, 0]])

##Assigned Test Cases END ##
                    
#Goal Puzzle
GOAL = np.array([[1, 2, 3],
                 [4, 5, 6],
                 [7, 8, 0]])
                 
#Temp Blank Puzzle
TEMP = np.array([[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]])

                 
##



#User input Board
def build():
    NumPrompt = ["First", "Second", "Third"]
    print("Enter your puzzle, use a zero to represent the blank \n")
    for i in range(3):
        print("Enter the",NumPrompt[i],"row, use space or tab between the three numbers: ")
        inNum = input()
        INIT[i] = inNum.split()
    return
    
#Auto create Board
def autofill():
    a = 0
    randVals = random.sample(range(9), 9)
    for i in range(3):
        for j in range(3):
            INIT[i][j] = randVals[a]
            a += 1
    return

#Counts number of misplaced tile, returns heuristic value
def misplaced(input_node):
    heuristic_count = 0
    for i in range(3):
        for j in range(3):
            if(input_node.data[i][j] != GOAL[i][j]):
                heuristic_count += 1
    return heuristic_count
    
#Evaluates the distance between tiles, returns heuristic value
def manhattan(input_node):
    heuristic_count = 0
    
    for i in range(1, 9):
        origin_location = np.argwhere(input_node.data == i)
        x1 = origin_location[0][0]
        y1 = origin_location[0][1]
        
        goal_location = np.argwhere(GOAL == i)
        x2 = goal_location[0][0]
        y2 = goal_location[0][1]
        
        distance = abs(x2 - x1) + abs(y2 - y1)
        heuristic_count += distance
    
    return heuristic_count

        
    
#Shifts 0 into desired direction
def shift(curr_node, direction):
    #Deep copy to fully copy the puzzle board
    new_board = copy.deepcopy(curr_node.data)

    #Finds the location of "0" on the board
    zeroloc = np.argwhere(curr_node.data == 0)
    x = zeroloc[0][0] # 2
    y = zeroloc[0][1]
    
    #print(new_board)
    if(direction == 1): #up
        if(x - 1 < 0):
            return curr_node.data
        else:
            new_board[x][y] = new_board[x-1][y]
            new_board[x-1][y] = 0
            return new_board
    if(direction == 2): #down
        if(x + 1 > 2):
            return curr_node.data
        else:
            new_board[x][y] = new_board[x+1][y]
            new_board[x+1][y] = 0
            return new_board
    if(direction == 3): #left
        if(y - 1 < 0):
            return curr_node.data
        else:
            new_board[x][y] = new_board[x][y-1]
            new_board[x][y-1] = 0
            return new_board
    if(direction == 4): #right
        if(y+1 > 2):
            return curr_node.data
        else:
            new_board[x][y] = new_board[x][y+1]
            new_board[x][y+1] = 0
            return new_board
    

        
        
#Search Function, takes in function to determine which one to use
def search(problem, function):
    queue = []
    visited = []
    priQ.heapify(queue)
    
    expand = 0
    max = 0
    depth = 0
    
    #Selects which search to use
    if(function == "1"):
        #print("Uniform Cost Search Selected.\n")
        problem.cost = 1
    if(function == "2"):
        #print("A* with Misplaced Tile Heuristic Selected.\n")
        problem.cost = 1
        problem.heuristic = misplaced(problem)
    if(function == "3"):
        #print("A* with Manhattan Distance Heuristic Selected.\n")
        problem.cost = 1
        problem.heuristic = manhattan(problem)
    
    priQ.heappush(queue, problem)
    
    while (len(queue) > 0):
        priQ.heapify(queue)
        #expand += 1
        if len(queue) > max:
            max = len(queue)
            
        curr = priQ.heappop(queue)
        
        #Use for text formatting
        if (curr.uniform != 0):
            print("The best state to expand with a g(n) =",curr.uniform,"and h(n) =",curr.heuristic, "is...")
            print(curr.data)
            print("Expanding this node...")
        else:
            print("Expanding state")
            print(curr.data)

        print("")
        if (curr.solved()):         #If answer is found
            depth = curr.uniform
            print("\nGoal!!!\n\n")
            print("To solve this problem the search algorithm expanded a total of", expand, "nodes.")
            print("The maximum number of nodes in the queue at any one time was", max,".")        #max queue size
            print("The Depth of the goal node was:", depth)      #number of moves to solve
            return;
        else:                       #Continue Search when Answer not found
            visited.append(curr)
            up = node(shift(curr, 1))
            down = node(shift(curr, 2))
            left = node(shift(curr, 3))
            right = node(shift(curr, 4))
            
            up.uniform = curr.uniform + 1
            down.uniform = curr.uniform + 1
            left.uniform = curr.uniform + 1
            right.uniform = curr.uniform + 1
            
            #misplaced
            if (function == "2"):
                up.heuristic = misplaced(up)
                down.heuristic = misplaced(down)
                left.heuristic = misplaced(left)
                right.heuristic = misplaced(right)
            #manhattan
            if (function == "3"):
                up.heuristic = manhattan(up)
                down.heuristic = manhattan(down)
                left.heuristic = manhattan(left)
                right.heuristic = manhattan(right)

            #Calculates cost with f(n) = g(n) + h(n)
            up.cost = up.uniform + up.heuristic
            down.cost = down.uniform + down.heuristic
            left.cost = left.uniform + left.heuristic
            right.cost = right.uniform + right.heuristic
            
            if not (up.isRepeat(visited)):
                #print("Up Not Repeat")
                priQ.heappush(queue, up)
                expand += 1
            if not (down.isRepeat(visited)):
                #print("Down Not Repeat")
                priQ.heappush(queue, down)
                expand += 1
            if not (left.isRepeat(visited)):
                #print("Left Not Repeat")
                priQ.heappush(queue, left)
                expand += 1
            if not (right.isRepeat(visited)):
                #print("Right Not Repeat")
                priQ.heappush(queue, right)
                expand += 1
                
    print("\nSearch Failed...\n\n")
    print("The search algorithm expanded a total of", expand,"nodes.\n")
    print("The maximum number of nodes in the queue at any one time was", max)
    return
        

#main#
print("Welcome to Alic Lien's 8-Puzzle Solver!\n")
print("Type '1' to use a default puzzle, or '2' to enter your own puzzle")

choice1 = input()
if(choice1 == "0"):     #Calls a randomly generated board
    autofill()
elif(choice1 == "1"):   #Default Puzzle
    INIT = DEFAULT
elif(choice1 == "2"):   #User Input Puzzle
    build()
elif(choice1 == "3"):   #Only used for Testing Given Cases
    print("!!!Dev Mode!!!, Choose a test between 1-6 for Trivial to Impossible:")
    choice3 = input();
    if(choice3 == "1"):
        print("TRIVIAL")
        INIT = TRIVIAL
    if(choice3 == "2"):
        print("VEASY")
        INIT = VEASY
    if(choice3 == "3"):
        print("EASY")
        INIT = EASY
    if(choice3 == "4"):
        print("DOABLE")
        INIT = DOABLE
    if(choice3 == "5"):
        print("OHBOY")
        INIT = OHBOY
    if(choice3 == "6"):
        print("IMPOSSIBLE")
        INIT = IMPOSSIBLE


#Initiate the Start and Goal nodes
StartNode = node(INIT)
GoalNode = node(GOAL)

print("\nEnter your choice of Algorithm: ")
print("   1. Uniform Cost Search")
print("   2. A* with Misplaced Tile Heuristic")
print("   3. A* with Manhattan Distance Heuristic")
choice2 = input()

search(StartNode, choice2)

