import sys # in order to access command line prompts





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
    # print(algorithm)
    # print(file)
    
    # this is sorta just all parcing data to be ready for the search
    #reading file
    path="Project_1/"+file
    with open(path, "r") as f:
        colNum = int(f.readline().strip())
        rowNum = int(f.readline().strip())
        grid = [list(f.readline().strip()) for i in range(rowNum)]
    
    # robotPos = None
    robotPos=None
    dirtyTiles = set()

    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == '@':
                robotPos = (r, c)
            elif grid[r][c] == '*':
                dirtyTiles.add((r, c))

    #from here set initial position and then you can choose whether to go into dfs and bfs, which will be functions 
    print(dirtyTiles)




if __name__ == "__main__":
    main()