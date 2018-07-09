from tkinter import *
from tkinter import messagebox
import time
import networkx as nx
import pandas as pd
import numpy as np
import random
'''import matplotlib.pyplot as plt'''
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as pet
from generate import r,c
SIZE=50
HEIGHT=r*SIZE
WIDTH=c*SIZE
valid=[]
id=[]
robot=[]
timec=0
timem=0
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
f=open('path.txt','r')
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
     un={}
     k=[]
     for i in df.index:
        un[i]=[]
        flag=0
        for j in df.index:
            if j!=i and df.loc[i,'current']==df.loc[j,'next']:
                un[i].append(j)
            if j!=i and df.loc[j,'current']==df.loc[i,'next']:
                flag=1
        if flag==0:
            k.append(i)
     '''generate bfs from dictionary'''
     for i in k:
        bfs=bfs_connected_component(un,i)
        for i in bfs:
          flag1=0
          flag2=0
          flag4=0
          for j in bfs:
              if j!=i and df.loc[i,'decision']!='X':
                if df.loc[i,'next']==df.loc[j,'current']:
                  
                        if (df.loc[j,'decision']=='A')or(df.loc[j,'decision']=='W'):
                            df.loc[i,'decision']='W'
                            flag2=1
                            break
                        elif df.loc[j,'decision']=='N':
                            df.loc[i,'decision']='N'
                            flag4=1
                elif df.loc[i,'next']==df.loc[j,'next']:
                   flag1=1
          if flag1==1 and flag2==0 and flag4==0:
                   x=df.loc[i,'next']
                   messagebox.showinfo("Title","Auction")
                   x=tuple(x)
                   if x not in dict:
                       dict[x]=[]
                   dict[x].append(i)
                   dict[x].append(j)
                   df.loc[i,'decision']='A'
          if flag2==0 and flag4==0 and flag1==0:
            df.loc[i,'decision']='M'
          if flag4==1:
            messagebox.showinfo("title","oh no!")
     
     for i in df.index:
        if df.loc[i,'decision']=='M':
            i.pos=i.pos+1
            move_robot(i,df)
            y=df.at[i,'next']
            df.at[i,'current']=y
            if i.pos<len(i.path):
               df.at[i,'next']=i.path[i.pos]
            elif i.pos==len(i.path):
               df.loc[i,'decision']="X"
               print("destination reached of ",i.id)
               df.drop(i,inplace=True)
            print(df)
        elif df.loc[i,'decision']=='A':
             auction(dict,df)
     canvas.update()
     time.sleep(1)

     if df.empty:
         print('finished')
         break

def move_robot(x,df):
    global timem
    current=df.loc[x,'current']
    nex=df.loc[x,'next']
    print(current,nex)
    start=time.time()
    if nex[0]-current[0]==1:
        canvas.move(x.id,0,SIZE)
    elif nex[0]-current[0]==-1:
        canvas.move(x.id,0,-SIZE)
    elif nex[1]-current[1]==1:
        canvas.move(x.id,SIZE,0)
    elif nex[1]-current[1]==-1:
        canvas.move(x.id,-SIZE,0)
    end=time.time()
    diff=end-start
    timem=timem+diff

def auction(dict,df):
    messagebox.showinfo("Title","Auction occured")
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
                move_robot(x,df)
                print("the robot has id",x)
                print("It's category is:",x.category)
                print("it has paid ",second_max)
            else:
                df.loc[x,'decision']='W'

def bfs_connected_component(graph, start):
    # keep track of all visited nodes
    explored = []
    # keep track of nodes to be checked
    queue = [start]

    levels = {}         # this dict keeps track of levels
    levels[start]= 0    # depth of start node is 0

    visited= [start]     # to avoid inserting the same node twice into the queue

    # keep looping until there are nodes still to be checked
    while queue:
       # pop shallowest node (first node) from queue
        node = queue.pop(0)
        explored.append(node)
        neighbours = graph[node]

        # add neighbours of node to queue
        for neighbour in neighbours:
            if neighbour not in visited:
                queue.append(neighbour)
                visited.append(neighbour)

                levels[neighbour]= levels[node]+1
                # print(neighbour, ">>", levels[neighbour])


    return explored


d=5
num=input("Enter number of robots: ")
num=int(num)
category=['premium','regular','economy']
color=['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']
sample1=random.sample(valid,num)
sample2=random.sample(valid,num)
sample3=random.sample(color,num)
print("sample 1 ",sample1)
print("sample 2 ",sample2)
for i in range(0,num):
    #a=random.choice(valid)
    #u=random.choice(valid)
    a=sample1[i]
    u=sample2[i]
    v=random.choice(category)
    t=sample3[i]
    print("source:",a)
    print("destination:",u)
    r1=Robot(v,a,u)
    robot.append(r1)
    r1.create_robot(t)
current=[]
next=[]
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
print(df.index)
print(type(df.index))
start=time.time()
df=log(df)
end=time.time()
diff=end-start
timec=timec+diff
print("timec ",timec-timem)
print("timem ",timem)
d=d-1
root.mainloop()
