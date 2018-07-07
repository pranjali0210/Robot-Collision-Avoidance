from tkinter import *
from tkinter import messagebox
import time
import networkx as nx
import pandas as pd
import random
import timeit
import matplotlib.pyplot as plt
from generate import r,c
SIZE=50
HEIGHT=r*SIZE
WIDTH=c*SIZE
valid=[]
id=[]
priority=[]
robot=[]
pos=1
root = Tk()
canvas = Canvas(root, bg="white", height=HEIGHT, width=WIDTH)
root.title("Decentralized Robot Collision Avoidance")
canvas.pack()


def draw_grid():
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

matrix=[[0]*c for i in range(r)]
f=open('route.txt','r')
while(1):
    flag=0
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
        flag=-1
        val=-1
    if s[x]=='B'and len(s)<=8:
        flag=-1
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
    if flag==0:
        x=[i,j]
        valid.append(x)

print(matrix)
f.close()

draw_grid()


for i in range(r):
    for j in range(c):
        if matrix[i][j]==-2:
            set_exit_points(i,j)
        if matrix[i][j]==-1:
            set_obstacles(i,j)

def shortest_path(matrix,source,target):
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
    if nx.has_path(G,s,t):
        a=nx.dijkstra_path(G,s,t)
    else:
        return -1
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
    #plt.show()
    return path

class Robot():

    def __init__(self,category,source,target):
        self.path=[]
        self.source=source
        self.target=target
        self.pos=1
        self.id=0
        self.bid=0

    def create_robot(self,color):
        self.id=canvas.create_rectangle(SIZE*(self.source[1]),SIZE*(self.source[0]),SIZE*(self.source[1]+1),SIZE*(self.source[0]+1),fill=color)
        self.path=shortest_path(matrix,self.source,self.target)
        self.color=color
        self.priority=len(self.path)*0.04



def log(df):
     ind=df.index
     ind=list(ind)
     for i in ind:
        #print('Priority',i.priority)
        #print("old path",i.path)
        for j in ind:
            if ind.index(i)>ind.index(j):
              if df.loc[i,'next']==df.loc[j,'current'] or df.loc[i,'next']==df.loc[j,'next']:
                 a=df.loc[i,'next']
                 print("a:",a)
                 current=df.loc[i,'current']
                 print("current:",current)
                 matrix1=matrix
                 temp=matrix1[a[0]][a[1]]
                 matrix1[a[0]][a[1]]=-1
                 path=shortest_path(matrix1,df.loc[i,'current'],i.target)
                 matrix1[a[0]][a[1]]=temp
                 if path==-1:
                     #messagebox.showinfo("Title","Waiting")
                     #df.loc[i,'decision']=="W"
                     k=i.path.index(current)
                     i.path.insert(k,current)
                 else:
                   #messagebox.showinfo("Title","Path changed")
                   i.path=i.path[0:i.path.index(current)]
                   for x in path:
                      i.path.append(x)

        print(i.priority,i.path)
def plan(df):
    while(1):
        log(df)
        for i in df.index:
          #if df.loc[i,'decision']!="W":
            i.pos=i.pos+1
            y=df.at[i,'next']
            df.at[i,'current']=y
            if i.pos<len(i.path):
               df.at[i,'next']=i.path[i.pos]
               print(df)
            elif i.pos==len(i.path):
               df.loc[i,'decision']="X"
               print("destination reached of ",i.id)
        count=0
        for i in df.index:
          if df.loc[i,'decision']=="X":
              count=count+1
        if count==len(robot):
          print('finished')
          break
    move_robot(df)


def move_robot(df):
    for i in df.index:
        print("path for ",i.id,i.path)
    j=0
    while(1):
        for i in df.index:
          if i.path[j+1][0]-i.path[j][0]==1:
            canvas.move(i.id,0,SIZE)
          elif i.path[j+1][0]-i.path[j][0]==-1:
            canvas.move(i.id,0,-SIZE)
          elif i.path[j+1][1]-i.path[j][1]==1:
            canvas.move(i.id,SIZE,0)
          elif i.path[j+1][1]-i.path[j][1]==-1:
            canvas.move(i.id,-SIZE,0)
          if i.path[j+1]==i.target:
              df.drop(i,inplace=True)
        canvas.update()
        time.sleep(0.5)
        j=j+1
        if df.empty:
            break

def auction(dict,df):
    maxi=0
    second_max=0
    k=dict.keys()
    for i in k:
        a=list(set(dict[i]))
        bid=[]
        for x in a:
            if x.category=='regular':
               x.bid=random.gauss(0.5,0.083)
            elif x.category=='premium':
               x.bid=random.gauss(0.75,0.083)
            else:
                x.bid=random.gauss(0.25,0.083)

            bid.append(x.bid)
        print(bid)
        maxi=max(bid)
        bid.remove(maxi)
        second_max=max(bid)
        auc={}
        for x in a:
            if x.bid==maxi:
                max_index=x
                print('highest:',maxi,x)
                print('second highest:',second_max)
                df.loc[x,'decision']='M'
                print("the robot has id",x)
                print("It's category is:",x.category)
                print("it has paid ",second_max)
            else:
                df.loc[x,'decision']='W'

num=input("Enter number of robots: ")
num=int(num)
category=['premium','regular','economy']
color=['blue','green','black','green','purple','yellow','grey','cyan']
for i in range(1,num+1):
    a=random.choice(valid)
    u=random.choice(valid)
    v=random.choice(category)
    t=random.choice(color)
    print("source:",a)
    print("destination:",u)
    if a!=u:
        r1=Robot(v,a,u)
        robot.append(r1)
        r1.create_robot(t)
current=[]
next=[]
for x in robot:
    current.append(x.path[0])
    next.append(x.path[1])
    id.append(x.id)
    priority.append(x.priority)

data={'id':id,'current':current,'next':next,'priority':priority}
df=pd.DataFrame(data,columns=['id','current','next','priority','decision'],index=robot)
df.sort_values('priority',ascending=False,inplace=True,axis=0)
print(df)
df=plan(df)
root.mainloop()
