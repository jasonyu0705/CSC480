import sys # in order to access command line prompts
from collections import deque
#dfs algorithm
def dfs(visited,path):
    global grid
    global robotPos
    global expandedNodes
    global generatedNodes
    row=robotPos[0]
    col=robotPos[1]
    expandedNodes+=1
    #base case for recursion. if the spot in te grid is dirty then clean it and return the path
    if grid[row][col] == '*':
        grid[row][col] = '-'
        return path+"V"
    #for each option to move, make sure that its a valid move and that the position has not been visited yet
    #if it is valid then add it to the visited set and call dfs again with the new position
    if 0<= row-1 < len(grid) and 0<= col < len(grid[0]) and grid[row-1][col] != '#' and (row-1,col) not in visited:
        robotPos=(row-1,col)
        visited.add(robotPos)
        findPath= dfs(visited,path+"N")
        generatedNodes+=1
        if findPath is not None:
            return findPath
    if 0<= row < len(grid) and 0<= col+1 < len(grid[0]) and grid[row][col+1] != '#'and (row,col+1) not in visited:
        robotPos=(row,col+1)
        visited.add(robotPos)
        findPath= dfs(visited,path+"E")
        generatedNodes+=1
        if findPath is not None:
            return findPath
    if 0<= row+1 < len(grid) and 0<= col < len(grid[0]) and grid[row+1][col] != '#'and (row+1,col) not in visited:
        robotPos=(row+1,col)
        visited.add(robotPos)
        findPath= dfs(visited,path+"S")
        generatedNodes+=1
        if findPath is not None:
            return findPath
    if 0<= row < len(grid) and 0<= col-1 < len(grid[0]) and grid[row][col-1] != '#'and (row,col-1) not in visited:
        robotPos=(row,col-1)
        visited.add(robotPos)
        findPath= dfs(visited,path+"W")
        generatedNodes+=1
        if findPath is not None:
            return findPath 
    return None

#essentially just BFS
def ucs(path):
    global grid
    global robotPos
    global expandedNodes
    global generatedNodes
    queue=deque()
    # counter=0
    queue.append((robotPos, "")) 
    visited={robotPos}

    # check some initial position too keep in the while loop
    #while 0<= row < len(grid) and 0<= col < len(grid[0]) and grid[row][col] != '#' :
    while queue:
        #print(visited)
        #pop the next node off the queue
        (row,col), path = queue.popleft()
        generatedNodes += 1
        robotPos=(row,col)
        #chack if its dirty or not and if so return the path up to the point of the dirty node
        if grid[row][col] == '*':
            grid[row][col] = '-'
            return path+"V" 
        # print("robot position "+str(robotPos))
        #for every position in the while loop, check to see whether the neighnbour is valid and if so then add it to the queue 
        for move in ['N', 'E', 'S', 'W']:
            if move == 'N' and 0<= row-1 < len(grid) and 0<= col < len(grid[0]) and grid[row-1][col] != '#' and (row-1,col) not in visited:
                queue.append(((row-1,col), path + "N"))
                expandedNodes += 1 
            if move == 'E' and 0<= row < len(grid) and 0<= col+1 < len(grid[0]) and grid[row][col+1] != '#' and (row,col+1) not in visited:
                queue.append(((row,col+1), path + "E"))
                expandedNodes += 1 
            if move == 'S' and 0<= row+1 < len(grid) and 0<= col < len(grid[0]) and grid[row+1][col] != '#' and (row+1,col) not in visited:
                queue.append(((row+1,col), path + "S"))
                expandedNodes += 1 
            if move == 'W' and 0<= row < len(grid) and 0<= col-1 < len(grid[0]) and grid[row][col-1] != '#' and (row,col-1) not in visited:
                queue.append(((row,col-1), path + "W")) 
                expandedNodes += 1 
        #add the current node to vidited 
        visited.add((row,col))
        # if counter==9:

    return None      

#global vars
grid = [[]]
robotPos=(0,0)
expandedNodes=0
generatedNodes=0

def main():
    global grid
    global robotPos
    steps=""
    
    testing= False
    # if statement that just makes testing easier
    if testing == True:
        algorithm = "uniform-cost"
        file = "sample-5x7.txt"
    if testing == False:
        if len(sys.argv) != 3:
            print("The following is the formatting python3 Project1.py [algorithm] [world-file]")
            sys.exit(1)
        algorithm = sys.argv[1]
        file = sys.argv[2]
    # this is sorta just all parcing data to be ready for the search
    #reading file
    #path="Project_1/"+file
    with open(file, "r") as f:
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


    #going into actual algorithm
    if algorithm == "depth-first":
        visitedSet=set()
        while(True):
            #print("before position "+str(robotPos))
            call=dfs( visitedSet,"")
            #print("after position "+str(robotPos))
            
            if call is not None:
                steps=steps+call
                visitedSet=set()
            else:
                break
        print("path: "+steps)
        print("expanded nodes: "+str(expandedNodes))
        print("generated nodes: "+str(generatedNodes))
    elif algorithm == "uniform-cost":

        while(True):
            call=ucs( "")
            #print("call is "+str(call))
            if call is not None:
                steps=steps+call
                
            else:
                break 
            
        print("path: "+steps)
        print("expanded nodes: "+str(expandedNodes))
        print("generated nodes: "+str(generatedNodes))
    else:
        print("Invalid input")
        
if __name__ == "__main__":
    main()