from tkinter import *
from tkinter import messagebox
import time
import networkx as nx
import pandas as pd
import numpy as np
import random
import timeit
import matplotlib.pyplot as plt
from generate import r,c,num,m,n
from colors import color
import sys
sys.stdout = open('output.txt','wt')
SIZE=50
HEIGHT=r*SIZE
WIDTH=c*SIZE
valid=[]
id=[]
priority=[]
robot=[]
pos=1
timem=0
timec=0
count=0
time_comp={}
time_move={}


matrix=[[0]*c for i in range(r)]
f=open('route.txt','r')
while(1):
    flag=0
    val=0
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

f.close()

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
       #print(x,y)
       path[i].append(x)
       path[i].append(y)
       i=i+1
    nx.draw(G)
    return path

class Robot():

    def __init__(self,source,target):
        self.path=[]
        self.source=source
        self.target=target
        self.pos=0
        self.id=0
        self.bid=0

    def create_robot(self,color):
        global timec
        #self.id=canvas.create_rectangle(SIZE*(self.source[1]),SIZE*(self.source[0]),SIZE*(self.source[1]+1),SIZE*(self.source[0]+1),fill=color)
        start=time.time()
        self.path=shortest_path(matrix,self.source,self.target)
        end=time.time()
        diff=end-start
        timec=timec+diff
        self.color=color
        self.priority=len(self.path)*0.04



def log(df):
     ind=df.index
     ind=list(ind)
     for i in ind:
        matrix1=[]
        for a in range(r):
            matrix1.append([])
            for b in range(c):
                x=matrix[a][b]
                matrix1[a].append(x)
        current=df.loc[i,'current']
        d=ind.index(i)
        flag1=0
        flag2=0
        for j in range(0,d):
                 i.pos=0
                 k=ind[j]
                 a=df.loc[k,'next']
                 #print("a:",a)
                 if a==i.target:
                    path=-1
                    flag1=1
                 if a==df.loc[i,'current']:
                    continue
                 matrix1[a[0]][a[1]]=-1
        if flag1!=1 and flag2!=1:
            path=shortest_path(matrix1,current,i.target)
        if path==-1:
            k=i.path.index(current)
            i.path.insert(k+1,current)
            i.pos=1
        if path!=-1:
            #messagebox.showinfo("Title","Path changed")
            i.path=i.path[0:i.path.index(current)]
            for x in path:
                i.path.append(x)
        print(i.priority,i.path)
def plan(df):
    global count
    while(1):
        count=count+1
        log(df)
        global timem
        start=time.time()
        for i in df.index:
            y=df.loc[i,'current']
            if y==i.target:
               df.loc[i,'decision']="X"
               df.drop(i,inplace=True)
               continue
            z=len(i.path)-1-i.path[::-1].index(y)
            if z>=len(i.path)-2:
                n=z+1
            else: n=z+2
            if i.pos==1:
                df.at[i,'current']=i.path[z]
                df.at[i,'next']=i.path[z+1]
            else:
                df.at[i,'current']=i.path[z+1]
                df.at[i,'next']=i.path[n]
            print("pos: ",i.priority,z)
        print(df)
        #for i in df.index:
          #if df.loc[i,'decision']=="X":
            #  count=count+1
        end=time.time()
        diff=end-start
        timem=timem+diff

        if df.empty:
          print('finished')
          break

for s in num:
 d=1
 time_comp[s]=[]
 time_move[s]=[]
 while(d>0):
  robot=[]
  timec=0
  timem=0
  count=0
  sample1=random.sample(valid,s)
  sample2=random.sample(valid,s)
  for i in range(0,s):
   a=sample1[i]
   u=sample2[i]
   if a==u:
       i=i-1
       continue
   #v=random.choice(category)
   t=random.choice(color)
   print("source:",a)
   print("destination:",u)
   r1=Robot(a,u)
   robot.append(r1)
   r1.create_robot(t)
  current=[]
  next=[]
  id=[]
  priority=[]
  for x in robot:
    current.append(x.source)
    if len(x.path)>1:
      next.append(x.path[1])
    else:
      x.pos=0
      next.append([])
    id.append(x.id)
    priority.append(x.priority)
  data={'id':id,'current':current,'next':next,'priority':priority}
  df=pd.DataFrame(data,columns=['id','current','next','priority','decision'],index=robot)
  df.sort_values('priority',ascending=False,inplace=True,axis=0)
  print(df)
  start=time.time()
  df=plan(df)
  end=time.time()
  timec=end-start
  timec=timec-timem
  print("Timec ",timec)
  print("Timem ",count)
  time_comp[s].append(timec)
  time_move[s].append(count)
  print("One iteration")
  d=d-1
 f=open('plots2.txt','a')
 f.write("Prioritised planning\n")
 x=time_comp[s]
 y=time_move[s]
 x=np.array(x)
 y=np.array(y)
 f.write("Grid size: %d\n"%m)
 f.write("No. of robots: %d\n" %s)
 f.write("Computation time:\n")
 f.write("%.15f\n"%np.mean(x))
 f.write("Movement time:\n")
 f.write("%d\n"%np.mean(y))
 f.close()
#root.mainloop()
