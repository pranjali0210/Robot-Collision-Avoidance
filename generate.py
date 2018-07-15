import numpy as np
m=input("Enter m")
m=int(m)
n=input("Enter n")
n=int(n)
#num=input("Enter number of robots: ")
num=[5,10,15,20,25,30]
r=5*n
c=5*m
arr=np.empty((r,c), dtype='object')
arr[0][0]='B'
arr[0][c-1]='B'
arr[r-1][c-1]='B'
arr[r-1][0]='B'
for i in range(1,r-1,5):
  for j in range(1,c-1,5):
    arr[i][j]='O'
    arr[i+1][j]='O'
    arr[i+2][j]='O'
    arr[i][j+1]='O'
    arr[i+1][j+1]='O'
    arr[i+2][j+1]='O'
    arr[i][j+2]='O'
    arr[i+1][j+2]='O'
    arr[i+2][j+2]='O'
for i in range(4,r-1,5):
  for j in range(c):
    if(j%5==4):
      arr[i][j]='RU'
      arr[i+1][j]='LU'
    elif(j%5==0):
      arr[i][j]='RD'
      arr[i+1][j]='LD'
    else:
      arr[i][j]='R'
      arr[i+1][j]='L'
for i in range(4,c-1,5):
  for j in range(1,r-1,5):
    arr[j][i]='U'
    arr[j+1][i]='U'
    arr[j+2][i]='U'
    arr[j][i+1]='D'
    arr[j+1][i+1]='D'
    arr[j+2][i+1]='D'
for x in range(1,c-1):
  if(arr[1][x]!='O'):
    if(arr[0][x-1]=='B'):
      arr[0][x]='R'
    else:
      arr[0][x]='D'
  else:
    arr[0][x]='B'
for x in range(1,r-1):
  if(arr[x][c-2]!='O'):
    if(arr[x-1][c-1]=='B'):
      arr[x][c-1]='D'
    else:
      arr[x][c-1]='L'
  else:
    arr[x][c-1]='B'
for x in range(1,c-1):
  if(arr[r-2][x]!='O'):
    if(arr[r-1][x-1]=='B'):
      arr[r-1][x]='U'
    else:
      arr[r-1][x]='L'
  else:
    arr[r-1][x]='B'
for x in range(1,r-1):
  if(arr[x][1]!='O'):
    if(arr[x-1][0]=='B'):
      arr[x][0]='R'
    else:
      arr[x][0]='U'
  else:
    arr[x][0]='B'
path='route.txt'
file=open(path,'w')
for i in range(r):
  for j in range(c):
    s=arr[i][j]
    file.write(str(i)+','+str(j)+':'+str(s)+'\n')
file.close()
