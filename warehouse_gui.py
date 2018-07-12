from tkinter import *
from tkinter import messagebox
import time
import numpy as np
import networkx as nx
import pandas as pd
import random
import matplotlib.pyplot as plt
from colors import color
from generate import r,c,num
#from plots import tc,tm
import sys
sys.stdout = open('output.txt','wt')
SIZE=50
HEIGHT=r*SIZE
WIDTH=c*SIZE
valid=[]
id=[]
robot=[]
timec=0
timem=0
time_comp={}
time_move={}
pos=1
root = Tk()
canvas = Canvas(root, bg="AntiqueWhite1", height=HEIGHT, width=WIDTH)
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
        x=canvas.create_rectangle(SIZE*j,SIZE*i,SIZE*(j+1),SIZE*(i+1),fill='red2')

def set_obstacles(x,y):
    a=canvas.create_rectangle(SIZE*(y),SIZE*(x),SIZE*(y+1),SIZE*(x+1),fill='brown4')

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
    #plt.show()
    return path

class Robot():

    def __init__(self,category,source,target):
        self.path=[]
        self.category=category
        self.source=source
        self.target=target
        self.pos=1
        self.id=0
        self.bid=0
        self.f=0

    def create_robot(self,color):
        global timec
        self.id=canvas.create_rectangle(SIZE*(self.source[1]),SIZE*(self.source[0]),SIZE*(self.source[1]+1),SIZE*(self.source[0]+1),fill=color)
        start=time.time()
        self.path=shortest_path(self.source,self.target)
        end=time.time()
        diff=end-start
        timec=timec+diff
        self.color=color



def log(df):
    while(1):
     dict={}
     for i in df.index:
        flag=0
        i.f=0
        for j in df.index:
            if j!=i and df.loc[i,'decision']!='X':
              if df.loc[i,'next']==df.loc[j,'current']:
                 df.loc[i,'decision']='W'
                 flag=-1
                 break
              elif df.loc[i,'next']==df.loc[j,'next']:
                   x=df.loc[i,'next']
                   #messagebox.showinfo("Title","Auction")
                   x=tuple(x)
                   if x not in dict:
                       dict[x]=[]
                   dict[x].append(i)
                   dict[x].append(j)
                   df.loc[i,'decision']='A'
                   flag=-1
                   #break

        if flag!=-1:
            df.loc[i,'decision']="M"
     for i in df.index:
        if df.loc[i,'decision']=='M'and i.f==0:
            k=df.loc[i,'next']
            s=0
            if matrix[k[0]][k[1]]==5:
                p=[k[0],k[1]+1]
                q=[k[0]-1,k[1]]
                r=[k[0]-1,k[1]+1]
                for j in df.index:
                    if j!=i:
                        if df.loc[j,'current']==p:
                            s=s+1
                        elif df.loc[j,'current']==q:
                            s=s+1
                        elif df.loc[j,'current']==r:
                            s=s+1
            elif matrix[k[0]][k[1]]==6:
                p=[k[0],k[1]-1]
                q=[k[0]-1,k[1]]
                r=[k[0]-1,k[1]-1]
                for j in df.index:
                    if j!=i:
                        if df.loc[j,'current']==p:
                            s=s+1
                        elif df.loc[j,'current']==q:
                            s=s+1
                        elif df.loc[j,'current']==r:
                            s=s+1
            elif matrix[k[0]][k[1]]==10:
                p=[k[0],k[1]-1]
                q=[k[0]+1,k[1]]
                r=[k[0]+1,k[1]-1]
                for j in df.index:
                    if j!=i:
                        if df.loc[j,'current']==p:
                            s=s+1
                        elif df.loc[j,'current']==q:
                            s=s+1
                        elif df.loc[j,'current']==r:
                            s=s+1
            elif matrix[k[0]][k[1]]==9:
                p=[k[0],k[1]+1]
                q=[k[0]+1,k[1]]
                r=[k[0]+1,k[1]+1]
                for j in df.index:
                    if j!=i:
                        if df.loc[j,'current']==p:
                            s=s+1
                        elif df.loc[j,'current']==q:
                            s=s+1
                        elif df.loc[j,'current']==r:
                            s=s+1
            if s==3:
                df.loc[i,'decision']="W"
                break
            i.pos=i.pos+1
            move_robot(i,df)
            y=df.at[i,'next']
            df.at[i,'current']=y
            if i.pos<len(i.path):
               df.at[i,'next']=i.path[i.pos]
               print(df)
            elif i.pos>=len(i.path):
               df.loc[i,'decision']="X"
               print("destination reached of ",i.id)
               df.drop(i,inplace=True)
               canvas.delete(i.id)
               print(df)
        elif df.loc[i,'decision']=='A':
             auction(dict,df)
        elif df.loc[i,'decision']=="X":
             df.drop(i,inplace=True)
             canvas.delete(i.id)
     canvas.update()
     time.sleep(0.5)

     if df.empty:
         print('finished')
         break

def move_robot(x,df):
    global timem
    current=df.loc[x,'current']
    next=df.loc[x,'next']
    print(current,next)
    start=time.time()
    if next[0]-current[0]==1:
        canvas.move(x.id,0,SIZE)
    elif next[0]-current[0]==-1:
        canvas.move(x.id,0,-SIZE)
    elif next[1]-current[1]==1:
        canvas.move(x.id,SIZE,0)
    elif next[1]-current[1]==-1:
        canvas.move(x.id,-SIZE,0)
    end=time.time()
    diff=end-start
    timem=timem+diff

def auction(dict,df):
    #messagebox.showinfo("Title","Auction occured")
    maxi=0
    second_max=0
    kx=dict.keys()
    for i in kx:  
                k=i
                l=list(set(dict[i]))
                s=0
                if matrix[k[0]][k[1]]==5:
                   p=[k[0],k[1]+1]
                   q=[k[0]-1,k[1]]
                   r=[k[0]-1,k[1]+1]
                   for j in df.index:
                            if df.loc[j,'current']==p:
                                if j in l:
                                   x=j
                                s=s+1
                            elif df.loc[j,'current']==q:
                                 if j in l:
                                   x=j
                                 s=s+1
                            elif df.loc[j,'current']==r:
                                if j in l:
                                   x=j
                                s=s+1
                elif matrix[k[0]][k[1]]==6:
                    p=[k[0],k[1]-1]
                    q=[k[0]-1,k[1]]
                    r=[k[0]-1,k[1]-1]
                    for j in df.index:
                            if df.loc[j,'current']==p:
                                if j in l:
                                   x=j
                                s=s+1
                            elif df.loc[j,'current']==q:
                                if j in l:
                                   x=j
                                s=s+1
                            elif df.loc[j,'current']==r:
                                if j in l:
                                   x=j
                                s=s+1
                elif matrix[k[0]][k[1]]==10:
                    p=[k[0],k[1]-1]
                    q=[k[0]+1,k[1]]
                    r=[k[0]+1,k[1]-1]
                    for j in df.index:
                            if df.loc[j,'current']==p:
                                if j in l:
                                   x=j
                                s=s+1
                            elif df.loc[j,'current']==q:
                                if j in l:
                                   x=j
                                s=s+1
                            elif df.loc[j,'current']==r:
                                if j in l:
                                   x=j
                                s=s+1
                elif matrix[k[0]][k[1]]==9:
                            p=[k[0],k[1]+1]
                            q=[k[0]+1,k[1]]
                            r=[k[0]+1,k[1]+1]
                            for j in df.index:
                                    if df.loc[j,'current']==p:
                                        if j in l:
                                           x=j
                                        s=s+1
                                    elif df.loc[j,'current']==q:
                                        if j in l:
                                           x=j
                                        s=s+1
                                    elif df.loc[j,'current']==r:
                                        if j in l:
                                           x=j
                                        s=s+1
                if s==3:
                    df.loc[x,'decision']="M"
                    for j in l:
                        if j!=x:
                           df.loc[j,'decision']="W"
                    return
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
    for x in a:
            
            if x.bid==maxi:
                max_index=x
                print('highest:',maxi,x)
                print('second highest:',second_max)
                df.loc[x,'decision']='M'
                x.f=1
                print("the robot has id",x)
                print("It's category is:",x.category)
                print("it has paid ",second_max)
             
                x.pos=x.pos+1
                move_robot(x,df)
                y=df.at[x,'next']
                df.at[x,'current']=y
                if x.pos<len(x.path):
                   df.at[x,'next']=x.path[x.pos]
                elif x.pos>=len(x.path):
                   df.loc[x,'decision']="X"
                   print("destination reached of ",x.id)
                   #df.drop(x,inplace=True)

            else:
                df.loc[x,'decision']='W'
                x.f=1
for s in num:
 d=10
 time_comp[s]=[]
 time_move[s]=[]
 category=['premium','regular','economy']
 while(d>0):
  robot=[]
  timec=0
  timem=0
  sample1=random.sample(valid,s)
  sample2=random.sample(valid,s)
  print("sample 1 ",sample1)
  print("sample 2 ",sample2)
  for i in range(0,s):
    a=sample1[i]
    u=sample2[i]
    v=random.choice(category)
    t=random.choice(color)
    print("source:",a)
    print("destination:",u)
    r1=Robot(v,a,u)
    robot.append(r1)
    r1.create_robot(t)
  current=[]
  next=[]
  id=[]
  for x in robot:
    current.append(x.path[0])
    if len(x.path)>1:
       next.append(x.path[1])
    else:
       x.pos=0
       next.append(x.path[0])
    id.append(x.id)
  data={'id':id,'current':current,'next':next}
  df=pd.DataFrame(data,columns=['id','current','next','decision'],index=robot)
  print(df)
  start=time.time()
  df=log(df)
  end=time.time()
  diff=end-start
  timec=timec+diff
  timec=timec-timem
  print("timec ",timec)
  print("timem ",timem)
  time_comp[s].append(timec)
  time_move[s].append(timem)
  d=d-1
 print(time_comp)
 print(time_move)
 f=open('plots1.txt','a')
 f.write("Second price auction\n")
 x=time_comp[s]
 y=time_move[s]
 x=np.array(x)
 y=np.array(y)
#f.write("Grid size: %dX%d"%num)
 f.write("No. of robots: %d\n" %s)
 f.write("Computation time:\n")
#for i in x:
 f.write("%.15f\n"%np.mean(x))
 f.write("%.15f\n"%np.std(x))
 f.write("Movement time:\n")
#for i in y:
 f.write("%.18f\n"%np.mean(y))
 f.write("%.18f\n"%np.std(y))   
 f.close()
 #root.mainloop()
