import time
import numpy as np
import networkx as nx
import pandas as pd
import random
import matplotlib.pyplot as plt
from colors import color
from generate import r,c,num
import sys
#sys.stdout = open('output.txt','wt')
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
count=0

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

    def create_robot(self,color,timec):
        global timec
        start=time.time()
        self.path=shortest_path(self.source,self.target)
        end=time.time()
        diff=end-start
        timec=timec+diff
        self.color=color
        return timec


def log(df,timem):
    global count
    while(1):
     count=count+1
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
                   x=tuple(x)
                   if x not in dict:
                       dict[x]=[]
                   dict[x].append(i)
                   dict[x].append(j)
                   df.loc[i,'decision']='A'
                   flag=-1
        if flag!=-1:
            df.loc[i,'decision']="M"
     for i in df.index:
        start=time.time()
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
                continue
            i.pos=i.pos+1
            y=df.at[i,'next']
            df.at[i,'current']=y
            if i.pos<len(i.path):
               df.at[i,'next']=i.path[i.pos]
               print(df)
            elif i.pos>=len(i.path):
               df.loc[i,'decision']="X"
               print("destination reached of ",i.id)
               df.drop(i,inplace=True)
               print(df)
        elif df.loc[i,'decision']=='A':
             auction(dict,df)
        elif df.loc[i,'decision']=="X":
             df.drop(i,inplace=True)
     end=time.time()
     diff=end-start
     timem=timem+diff
     if df.empty:
         print('finished')
         break
    return timem

def auction(dict,df):
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
                    continue
        a=list(set(dict[i]))
        print("auction: ",a)
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
                #print('highest:',maxi,x)
                #print('second highest:',second_max)
                df.loc[x,'decision']='M'
                x.f=1
                #print("the robot has id",x)
                #print("It's category is:",x.category)
                #print("it has paid ",second_max)
                x.pos=x.pos+1
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
def second_price(sample1,sample2,s):
  category=['premium','regular','economy']
  robot=[]
  timec=0
  timem=0
  for i in range(0,s):
    a=sample1[i]
    u=sample2[i]
    v=random.choice(category)
    t=random.choice(color)
    r1=Robot(v,a,u)
    robot.append(r1)
    timec=r1.create_robot(t,timec)
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
  df,timem=log(df)
  end=time.time()
  diff=end-start
  timec=timec+diff
  timec=timec-timem
  print("timec ",timec)
  print(timec)
  print(count)
  return timec,count
  """f=open('plots1.txt','a')
 f.write("Second price auction\n")
 x=time_comp[s]
 y=time_move[s]
 x=np.array(x)
 y=np.array(y)
 #f.write("Grid size: %dX%d"%num)
 f.write("No. of robots: %d\n" %s)
 f.write("Computation time:\n")
 f.write("%.15f\n"%np.mean(x))
 f.write("%.15f\n"%np.std(x))
 f.write("Movement time:\n")
 f.write("%d\n"%np.mean(y))
 #f.write("%\n"%np.std(y))
 f.close()"""
