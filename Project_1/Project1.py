import sys # in order to access command line prompts
from collections import deque

def dfs(robotPos, grid, finishedPath , visited, expandedNodes,generatedNodes):
    expandedNodes+=1
    # Check if there's any dirty tile left --> idk if im allowed to use this
    if not any('*' in row for row in grid):  
        return finishedPath
    #add the node your looking at to visited set
    visited.add(robotPos)
    for move in ['N','E','S','W','V']:#for each move to the action adn then recursively call dfs
        newRowPos=robotPos[0]
        newColPos=robotPos[1]
        if move == 'N': newRowPos-=1
        elif move == 'E':newColPos+=1
        elif move == 'S':newRowPos+=1
        elif move == 'W':newColPos-=1
        elif move == 'V':
            if grid[newRowPos][newColPos] == '*':# if the tile is dirty then clean it
                grid[newRowPos][newColPos] == '-'
            #reset the position if ur cleaning you shouldnt move
            newRowPos, newColPos = robotPos
        # if ur not making an illegal move and your not blocking anything then 
        if 0<= newRowPos < len(grid) and 0<= newColPos < len(grid[0]) and grid[newRowPos][newColPos] != '#':
            newRobotPos=(newRowPos,newColPos)
            # if the new position not in visited set then incrument genetrated nodes
            if newRobotPos not in visited:
                generatedNodes+=1
                print("finishedPath",finishedPath)
                print("move made",move)
                #recursively call DFS with the only difference being adding the move to the finished path
                
                steps=dfs(newRobotPos, grid, finishedPath+ [move], visited, expandedNodes,generatedNodes)
                if steps is not None:
                    return steps
    return None

#essentially just BFS
def ucs(robotPos,dirtyTiles, grid, finishedPath, expandedNodes,generatedNodes):
    queue = deque([(robotPos, [])])  # (current position, path taken to get here)
    visited = set()
    visited.add(robotPos)
    return None


def main():
    testing= True
    # if statement that just makes testing easier
    if testing == True:
        algorithm = "depth-first"
        file = "sample-5x7.txt"
    if testing == False:
        if len(sys.argv) != 3:
            print("Usage: python3 planner.py [algorithm] [world-file]")
            sys.exit(1)
        algorithm = sys.argv[1]
        file = sys.argv[2]
    # this is sorta just all parcing data to be ready for the search
    #reading file
    path="Project_1/"+file
    with open(path, "r") as f:
        colNum = int(f.readline().strip())
        rowNum = int(f.readline().strip())
        grid = [list(f.readline().strip()) for i in range(rowNum)]

    robotPos=None

    #looking through all positions and looking for the dirty tiles and the position of the robot
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@':
                robotPos = (row, col)
    #from here set initial position and then you can choose whether to go into dfs and bfs, which will be functions 

    expandedNodes=0
    generatedNodes=0
    #going into actual algorithm
    if algorithm == "depth-first":
        visitedSet=set()
        steps=dfs(robotPos, grid, [], visitedSet, expandedNodes,generatedNodes)
        print(steps)
        print("DFS")
    elif algorithm == "uniform-cost":
        #call UCS
        print("UCS")
    else:
        print("Invalid input")
        
        



if __name__ == "__main__":
    main()