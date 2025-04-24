import sys # in order to access command line prompts
from collections import deque

def dfs(visited,path, expandedNodes,generatedNodes):
    global grid
    global robotPos
    expandedNodes+=1
    row=robotPos[0]
    col=robotPos[1]
    if grid[row][col] == '*':
        grid[row][col] = '-'
        return path+"V"
    
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

#essentially just BFS
def ucs(path, expandedNodes,generatedNodes):
    global grid
    global robotPos
    global queue
    counter=0
    queue.append((robotPos, "")) 
    visited={robotPos}
    generatedNodes += 1
    # check some initial position too keep in the while loop
    #while 0<= row < len(grid) and 0<= col < len(grid[0]) and grid[row][col] != '#' :
    while queue:
        (row,col), path = queue.popleft()
        expandedNodes += 1 
        robotPos=(row,col)
        if grid[row][col] == '*':
            grid[row][col] = '-' 
            return path+"V" 
        print("robot position "+str(robotPos))
        print("asrdasdasdasdasd     "+str(queue))
        #for every position in the while loop, check to see whether the neighnbour is valid and if so then add it to the queue 
        for move in ['N', 'E', 'S', 'W']:
            if move == 'N' and 0<= row-1 < len(grid) and 0<= col < len(grid[0]) and grid[row-1][col] != '#' and (row-1,col) not in visited:
                #robotPos=(row-1,col)
                queue.append(((row-1,col), path + "N"))

            if move == 'E' and 0<= row < len(grid) and 0<= col+1 < len(grid[0]) and grid[row][col+1] != '#' and (row,col+1) not in visited:
                #robotPos=(row,col+1)
                queue.append(((row,col+1), path + "E"))

            if move == 'S' and 0<= row+1 < len(grid) and 0<= col < len(grid[0]) and grid[row+1][col] != '#' and (row+1,col) not in visited:
                #robotPos=(row+1,col)
                queue.append(((row+1,col), path + "S"))

            if move == 'W' and 0<= row < len(grid) and 0<= col-1 < len(grid[0]) and grid[row][col-1] != '#' and (row,col-1) not in visited:
                #robotPos=(row,col-1)
                queue.append(((row,col-1), path + "W")) 
            print(queue)
        if counter == 2:
            break  
        counter+=1
    return None      


# # Check if the new position is within bounds and not blocked
            # if 0 <= newRowPos < len(grid) and 0 <= newColPos < len(grid[0]) and grid[newRowPos][newColPos] != '#':
            #     newRobotPos = (newRowPos, newColPos)  # New robot position
            # queue.append((newRobotPos, path + [move]))
grid = [[]]
robotPos=(0,0)
queue=deque()
def main():
    global grid
    global robotPos
    steps=""
    
    testing= True
    # if statement that just makes testing easier
    if testing == True:
        algorithm = "uniform-cost"
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
    elif algorithm == "uniform-cost":
        #visitedSet=set()
        while(True):
            print("before position "+str(robotPos))
            call=ucs( "", expandedNodes,generatedNodes)#visited set
            print("after position "+str(robotPos))
            if call is not None:
                steps=steps+call
                #visitedSet=set()
            else:
                break 
        print("asdasdasdasdas      "+steps)
    else:
        print("Invalid input")
        
if __name__ == "__main__":
    main()