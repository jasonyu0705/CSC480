import sys # in order to access command line prompts
from collections import deque

def dfs(visited,path, expandedNodes,generatedNodes):
    global grid
    global robotPos
    expandedNodes+=1
    row=robotPos[0]
    col=robotPos[1]
    if grid[row][col] == '*':# if the tile is dirty then clean it
        grid[row][col] = '-'
        return path+"V"
    
    print(len(grid))
    print(len(grid[0]))
    print(row)
    print(col)
    if 0<= row-1 < len(grid) and 0<= col < len(grid[0]) and grid[row-1][col] != '#' and (row-1,col) not in visited:
        robotPos=(row-1,col)
        visited.add(robotPos)
        findPath= dfs(visited,path+"N", expandedNodes,generatedNodes)
        if findPath is not None:
            return findPath
    if 0<= row < len(grid) and 0<= col+1 < len(grid[0]) and grid[row][col+1] != '#'and (row,col+1) not in visited:
        robotPos=(row,col+1)
        visited.add(robotPos)
        findPath= dfs(  visited,path+"E", expandedNodes,generatedNodes)
        if findPath is not None:
            return findPath
    if 0<= row+1 < len(grid) and 0<= col < len(grid[0]) and grid[row+1][col] != '#'and (row+1,col) not in visited:
        robotPos=(row+1,col)
        visited.add(robotPos)
        findPath= dfs(  visited,path+"S", expandedNodes,generatedNodes)
        if findPath is not None:
            return findPath
    if 0<= row < len(grid) and 0<= col-1 < len(grid[0]) and grid[row][col-1] != '#'and (row,col-1) not in visited:
        robotPos=(row,col-1)
        visited.add(robotPos)
        findPath= dfs(  visited,path+"W", expandedNodes,generatedNodes)
        if findPath is not None:
            return findPath 

    return None
   

    # newRobotPos=(newRowPos,newColPos)
    # # if the new position not in visited set then incrument genetrated nodes
    # if newRobotPos not in visited:
    #     generatedNodes+=1
    #     print("move made",move)
    #     #recursively call DFS with the only difference being adding the move to the finished path
        

    #     if steps is not None:
    #         return steps
    # return None

#essentially just BFS
def ucs(robotPos,dirtyTiles, grid, finishedPath, expandedNodes,generatedNodes):
    queue = deque([(robotPos, [])])  # (current position, path taken to get here)
    visited = set()
    visited.add(robotPos)
    return None

grid = [[]]
robotPos=(0,0)
def main():
    global grid
    global robotPos
    steps=""
    
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
        while(True):
            print("before position "+str(robotPos))
            call=dfs( visitedSet,"", expandedNodes,generatedNodes)
            print("after position "+str(robotPos))
            
            if call is not None:
  
                steps=steps+call

                visitedSet=set()
            else:
                break
        print("asdasdasdasdas      "+steps)
        print("DFS")
    elif algorithm == "uniform-cost":
        #call UCS
        print("UCS")
    else:
        print("Invalid input")
        
if __name__ == "__main__":
    main()