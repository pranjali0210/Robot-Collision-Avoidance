from tkinter import *
import time
import networkx as nx
import matplotlib.pyplot as plt
HEIGHT=1000
WIDTH=1000
ROW_COUNT=10
COLUMN_COUNT=10
SIZE=100
root = Tk()
canvas = Canvas(root, bg="white", height=HEIGHT, width=WIDTH)
root.title("Decentralized Robot Collision Avoidance")
canvas.pack()

def draw_grid():
    row=[]
    column=[]
    for i in range(ROW_COUNT+1):
           x=canvas.create_line(0,SIZE*i,1000,SIZE*i,tag='row')   #row ID's from 1-41
    for i in range(COLUMN_COUNT+1):
           y=canvas.create_line(SIZE*i,0,SIZE*i,1000,tag='column')

def set_exit_points(i,j):
        x=canvas.create_rectangle(SIZE*j,SIZE*i,SIZE*(j+1),SIZE*(i+1),fill='red')

def set_obstacles(x,y):
    a=canvas.create_rectangle(SIZE*(y),SIZE*(x),SIZE*(y+1),SIZE*(x+1),fill='brown')



def move_robot(robot,path):
    for i in range(1,len(path)):
        if path[i][0]-path[i-1][0]==1:
            canvas.move(robot,0,SIZE)
        elif path[i][0]-path[i-1][0]==-1:
            canvas.move(robot,0,-SIZE)
        elif path[i][1]-path[i-1][1]==1:
            canvas.move(robot,SIZE,0)
        elif path[i][1]-path[i-1][1]==-1:
            canvas.move(robot,-SIZE,0)
        canvas.update()
        time.sleep(1)

matrix=[[0]*10 for i in range(10)]
f=open('path.txt','r')
while(1):
    val=0
    s=f.readline()
    if ""==s:
        break
    if len(s)==6:
       if s[4]=='L':
          val=4
       if s[4]=='R':
          val=8
       if s[4]=='U':
          val=1
       if s[4]=='D':
          val=2
       if s[4]=='O':
          val=-1
       if s[4]=='B':
          val=-2
    elif len(s)==7:
       if s[4]=='L' and s[5]=='U':
          val=5
       if s[4]=='L'and s[5]=='D':
          val=6
       if s[4]=='R' and s[5]=='U':
          val=9
       if s[4]=='R' and s[5]=='D':
          val=10
    i=int(s[0])
    j=int(s[2])
    matrix[i][j]=val

f.close()
draw_grid()
robot=canvas.create_rectangle(SIZE*4,0,SIZE*5,100,fill='blue')
for i in range(10):
    for j in range(10):
        if matrix[i][j]==-2:
            set_exit_points(i,j)
        if matrix[i][j]==-1:
            set_obstacles(i,j)
G=nx.DiGraph()
G.add_nodes_from([1,10*10])
for b in range(1,100+1):
  x=(b-1)/10
  y=(b-1)%10
  val=matrix[int(x)][int(y)]
  if(val<=0):
    continue
  if(val>=8):
    val-=8
    G.add_edge(b,b+1,weight=1)
  if(val>=4):
    val-=4
    G.add_edge(b,b-1,weight=1)
  if(val>=2):
    val-=2
    G.add_edge(b,b+10,weight=1)
  if(val>=1):
    val-=1
    G.add_edge(b,b-10,weight=1)
path=[]
source=(0,4)
target=(7,4)
s=10*source[0] + source[1] +1
t=10*target[0] + target[1] +1
a=nx.dijkstra_path(G,s,t)
i=0
for b in a:
  path.append([])
  x=(b-1)/10
  x=int(x)
  y=(b-1)%10
  print(x,y)
  path[i].append(x)
  path[i].append(y)
  i=i+1
nx.draw(G)
move_robot(robot,path)
plt.show()
root.mainloop()
