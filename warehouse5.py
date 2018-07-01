from tkinter import *
import time
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from generate import r,c
SIZE=50
HEIGHT=r*SIZE
WIDTH=c*SIZE
id=[]
robot=[]
pos=1
root = Tk()
canvas = Canvas(root, bg="white", height=HEIGHT, width=WIDTH)
root.title("Decentralized Robot Collision Avoidance")
canvas.pack()


def draw_grid():
    print(HEIGHT)
    print(WIDTH)
    row=[]
    column=[]
    for i in range(r+1):
           x=canvas.create_line(0,SIZE*i,WIDTH,SIZE*i,tag='row')
    for i in range(c+1):
           y=canvas.create_line(SIZE*i,0,SIZE*i,HEIGHT,tag='column')

def set_exit_points(i,j):
        x=canvas.create_rectangle(SIZE*j,SIZE*i,SIZE*(j+1),SIZE*(i+1),fill='red')

def set_obstacles(x,y):
    a=canvas.create_rectangle(SIZE*(y),SIZE*(x),SIZE*(y+1),SIZE*(x+1),fill='brown')



"""def move_robot(robot,path):
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
        time.sleep(1)"""

matrix=[[0]*c for i in range(r)]
f=open('route.txt','r')
while(1):
    val=80
    s=f.readline()
    if ""==s:
        break
    if s[2]==',':
        if s[5]==':':
            x=6
            i=10*int(s[0])+int(s[1])
            j=10*int(s[3])+int(s[4])
        elif s[4]==':':
            x=5
            i=10*int(s[0])+int(s[1])
            j=int(s[3])
    elif s[1]==',':
         if s[4]==':':
             x=5
             i=int(s[0])
             j=10*int(s[2])+int(s[3])
         elif s[3]==':':
             x=4
             i=int(s[0])
             j=int(s[2])
    if s[x]=='L'and len(s)<=8:
        val=4
    if s[x]=='R'and len(s)<=8:
        val=8
    if s[x]=='U'and len(s)<=8:
        val=1
    if s[x]=='D'and len(s)<=8:
        val=2
    if s[x]=='O'and len(s)<=8:
        val=-1
    if s[x]=='B'and len(s)<=8:
        val=-2
    if s[x]=='L' and s[x+1]=='U':
        val=5
    if s[x]=='L'and s[x+1]=='D':
        val=6
    if s[x]=='R' and s[x+1]=='U':
        val=9
    if s[x]=='R' and s[x+1]=='D':
        val=10
    matrix[i][j]=val

f.close()

draw_grid()


for i in range(r):
    for j in range(c):
        if matrix[i][j]==-2:
            set_exit_points(i,j)
        if matrix[i][j]==-1:
            set_obstacles(i,j)

def shortest_path(source,target):
    G=nx.DiGraph()
    G.add_nodes_from([1,r*c])
    for b in range(1,r*c+1):
        x=(b-1)/c
        y=(b-1)%c
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
           G.add_edge(b,b+c,weight=1)
        if(val>=1):
           val-=1
           G.add_edge(b,b-c,weight=1)
    path=[]
    s=c*source[0] + source[1] +1
    t=c*target[0] + target[1] +1
    a=nx.dijkstra_path(G,s,t)
    i=0
    for b in a:
       path.append([])
       x=(b-1)/c
       x=int(x)
       y=(b-1)%c
       print(x,y)
       path[i].append(x)
       path[i].append(y)
       i=i+1
    nx.draw(G)
    print(path)
    plt.show()
    return path

class Robot():

    def __init__(self,category,source,target):
        self.path=[]
        self.category=category
        self.source=source
        self.target=target
        self.pos=1
        self.id=0

    def create_robot(self,color):
        self.id=canvas.create_rectangle(SIZE*(self.source[1]),SIZE*(self.source[0]),SIZE*(self.source[1]+1),SIZE*(self.source[0]+1),fill=color)
        self.path=shortest_path(self.source,self.target)



def log(df):
    t=0
    flag=-1
    while(1):
     for i in df.index:
        for j in df.index:
            if j!=i and df.loc[i,'decision']!='X':
              if df.loc[i,'next']==df.loc[j,'current']:
                 df.loc[i,'decision']='W'
                 break
              elif df.loc[i,'next']==df.loc[j,'next']:
                   #call auction mechanism
                   #flag=1
                   break
              else:
                  df.loc[i,'decision']="M"
     for i in df.index:
        if df.loc[i,'decision']=='M':
            i.pos=i.pos+1
            move_robot(i,df)
            df.loc[i,'current']=df.loc[i,'next']
            if i.pos<len(i.path):
               df.loc[i,'next']=i.path[i.pos]
               print(df)
            elif i.pos==len(i.path):
               df.loc[i,'decision']="X"
               print(df)
     count=0
     for i in df.index:
         if df.loc[i,'decision']=='X':
            count=count+1
            print('c:',count)
     if count==len(robot):
         print("finished")
         return df

def move_robot(x,df):
    current=df.loc[x,'current']
    next=df.loc[x,'next']
    print(current,next)
    if next[0]-current[0]==1:
        canvas.move(x.id,0,SIZE)
    elif next[0]-current[0]==-1:
        canvas.move(x.id,0,-SIZE)
    elif next[1]-current[1]==1:
        canvas.move(x.id,SIZE,0)
    elif next[1]-current[1]==-1:
        canvas.move(x.id,-SIZE,0)
    canvas.update()
    time.sleep(0.075)

#def auction(i,j):

r1=Robot('premium',(0,4),(10,2))
robot.append(r1)
r1.create_robot('blue')
r2=Robot('premium',(4,0),(4,8))
robot.append(r2)
r2.create_robot('green')
r3=Robot('premium',(10,14),(6,9))
robot.append(r3)
r3.create_robot('black')
current=[]
next=[]
for x in robot:
    current.append(x.path[0])
    next.append(x.path[1])
    id.append(x.id)

data={'id':id,'current':current,'next':next}
df=pd.DataFrame(data,columns=['id','current','next','decision'],index=robot)
print(df)
df=log(df)
root.mainloop()
