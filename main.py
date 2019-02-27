## ANA* Algorithm

# import libraries
from sys import version_info
if version_info.major == 2:
    # We are using Python 2.x
    from Tkinter import *
    import ttk
elif version_info.major == 3:
    # We are using Python 3.x
    from tkinter import *
    from tkinter import ttk

import time 
import numpy as np
import math

G=1e10
E=1e10
openl=[]
succ=[]
optimalp=[]
applist=[]
grid=[]


class nodes:
    def __init__(self, val, x, y):
        self.color = val
        self.x = x
        self.y = y
        self.e = None
        self.g = 1e10  # a very high value
        self.h = None  # use Euclidean distance as heuristic
        self.f = None
        self.parent = None

'''
Define the color scheme for visualization. You may change it but I recommend using the same colors
'''
# white (0) is an unvisited node, black(1) is a wall, blue(2) is a visited node
# yellow(3) is for start node, green(4) is for exit node, red (5) is a node on the completed path
colors = {5: "red", 4: "green", 3: "yellow", 2: "blue", 1: "black", 0: "white"}


'''
Opens the maze file and creates tkinter GUI object
'''
# load maze
with open("easy.txt") as text:
    maze = [list(line.strip()) for line in text]


[col, row] = np.shape(maze)

root = Tk()
size = 700 / row
canvas = Canvas(root, width=(size*row), height=(size*col))
root.title("ANA* Algorithm")

def draw_canvas(canvas, maze):
    '''
Function to draw the grid and plot the solution
    '''
    
    for i in range(0, col):
        for j in range(0, row):
            canvas.create_rectangle(j*size, i*size, (j+1)*size, (i+1)*size, fill=colors[int(maze[i][j])])
    canvas.pack()


def calc_e(G,g,h):
    e=(G-g)/(h+1e-15)
    #print(e)
    return e

def calc_h(curr_x,curr_y,end_x,end_y):
    h=math.sqrt((end_x-curr_x)**2+(end_y-curr_y)**2)
    #print(h)
    return h


def find_emax(openl,G):
    
    all_e=[]
    for i in range (0,len(openl)):
        all_e.append(openl[i].e) 
    idx=np.argmax(all_e) 
    return idx


def find_idx(grid,x,y):
    
    for i in range(0,len(grid)):
        if grid[i].x==x and grid[i].y==y:
            idx=i
    return idx


def ana_star_code(start_node, exit_node):
    
    global G,E,openl,grid,succ,optimalp

    root.update()

    while len(openl)!=0:
        flag=0

        for i in range (0,len(openl)):
            openl[i].h=calc_h(openl[i].x,openl[i].y,exit_node[0],exit_node[1])
            openl[i].e=calc_e(G,openl[i].g,openl[i].h)


        idxx=find_emax(openl,G)
        curr_node=openl[idxx]# current node is a node with highest e in the open list
        
        del openl[idxx]

        if curr_node.e<E: # update E
           
            E=curr_node.e
           
        if curr_node.color=="4": #Update G
            G=curr_node.g

            preds=curr_node.parent # predecessor
            
            while(preds!=None):
                optimalp.append(preds)
                preds=preds.parent
        
            break



        succ=[]
        pos=find_idx(grid,curr_node.x,curr_node.y)
        #print(pos)
        for i in range(0,len(grid)):
            if i!=pos:
                if ((grid[i].x == grid[pos].x and grid[i].y == grid[pos].y+1) or (grid[i].x == grid[pos].x and grid[i].y == grid[pos].y-1) or (grid[i].x == grid[pos].x+1 and grid[i].y == grid[pos].y) or (grid[i].x == grid[pos].x-1 and grid[i].y == grid[pos].y)):
                    if grid[i].color!="1":
                        succ.append(grid[i])



        for i in range (0,len(succ)):
            succ[i].h=calc_h(succ[i].x,succ[i].y,exit_node[0],exit_node[1])
            succ[i].e=calc_e(G,succ[i].g,succ[i].h)

        for i in range (0,len(succ)):
            if curr_node.g+1<succ[i].g:
                succ[i].g=curr_node.g+1
                succ[i].parent=curr_node
                
                if succ[i].g+succ[i].h<G:
                    openl.append(succ[i])





def main():
    start_time=time.time()
    global G,E,openl,grid

    #print(row)
    #print(col)
    
    entrance_node = (row-1, 1)
    exit_node =(0, col-2)
    maze[entrance_node[0]][entrance_node[1]]="3"
    maze[exit_node[0]][exit_node[1]]="4"

    ent_node=nodes("3",row-1, 1)
    ex_node=nodes("4",0, col-2)




    # Make nodes of all rectangles
    for i in range(0,row):
        for j in range (0,col):
            grid.append(nodes(maze[i][j],i,j))

    first=find_idx(grid,entrance_node[0],entrance_node[1])
    grid[first].g=0
    grid[first].h=calc_h(grid[first].x,grid[first].y,exit_node[0],exit_node[1])
    grid[first].e=calc_e(G,grid[first].g,grid[first].h)
    
    openl.append(grid[first])

    while len(openl)!=0:
        
        
        ana_star_code(entrance_node,exit_node)
        
        for i in range (0,len(openl)):
            idx=find_idx(grid,openl[i].x,openl[i].y)
            #grid[idx].color="2"
    
        
        for i in range (0,len(openl)):
            openl[i].e=calc_e(G,openl[i].g,openl[i].h)
       
        for index,nd in enumerate(openl):
           if nd.g+nd.h>=G:
               x=openl.pop(index) 
    





    i=0
    for j in range(0,row):
        for k in range (0,col):
            maze[j][k]=grid[i].color
            i=i+1

    for m in range (0,len(optimalp)):
        for i in range(0,row):
            for j in range (0,col):
                if i==optimalp[m].x and j==optimalp[m].y:
                    maze[i][j]="2"
    flag=0
    t=0
    i=len(optimalp)-1
    while flag==0:
        if optimalp[i].x==optimalp[len(optimalp)-1].x and optimalp[i].y==optimalp[len(optimalp)-1].y and i!=len(optimalp)-1:
            
            flag=1
        else:
            for l in range(0,row):
                for m in range (0,col):
                    if l==optimalp[i].x and m==optimalp[i].y:
                        t=t+1
                        maze[l][m]="5"
        i=i-1
    
    # for i in range (0,len(optimalp)):
    #    print("optimal path",optimalp[i].x," ",optimalp[i].y)
        
   
    
        
    draw_canvas(canvas,maze)
    total_time=time.time()-start_time
    print("Total time:",total_time)
    print("Total nodes used for finding all solutions",len(optimalp))
            
    root.mainloop()
    

if __name__ == '__main__':
    main()