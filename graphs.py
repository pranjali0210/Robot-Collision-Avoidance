import matplotlib.pyplot as plt
import numpy as np
from warehouse_noGui import valid,second_price
from priority_noGui import pp
import random
from generate import num
import sys

timecomp_a={}
timemove_a={}
timecomp_p={}
timemove_p={}
std_a={}
std_p={}
for s in num:
     sample1=random.sample(valid,s)
     sample2=random.sample(valid,s)
     timecomp_a[s]=[]
     timemove_a[s]=[]
     timecomp_p[s]=[]
     timemove_p[s]=[]
     d=10
     while(d>0):
         innertimec_A,innertimem_A=second_price(sample1,sample2,s)
         print("auction ",innertimec_A,innertimem_A)
         timecomp_a[s].append(innertimec_A)
         timemove_a[s].append(innertimem_A)
         #innertimec_P,innertimem_P=pp(sample1,sample2,s)
         #print("Priority ",innertimec_P,innertimem_P)
         #timecomp_p[s].append(innertimec_P)
         #timemove_p[s].append(innertimem_P)
         d=d-1
     f=open("plots1.txt",'a')
     #p=open("plots2.txt",'a')
     x1=timecomp_a[s]
     y1=timemove_a[s]
     x1=np.array(x1)
     y1=np.array(y1)
     timecomp_a[s]=np.mean(x1)
     timemove_a[s]=np.mean(y1)
     #x2=timecomp_p[s]
     #y2=timemove_p[s]
     #x2=np.array(x2)
     #y2=np.array(y2)
     #timecomp_p[s]=np.mean(x2)
     #timemove_p[s]=np.mean(y2)
     std_a[s]=np.std(x1)
     #std_p[s]=np.std(x2)
#f.write("Grid size: %dX%d"%num)
     f.write( "%d\n" %s)
     #f.write("Computation time: auction\n")
     f.write("%.15f\n"%np.mean(x1))
     f.write("%.15f\n"%np.std(x1))
     #f.write("Movement time:auction\n")
     f.write("%d\n"%np.mean(y1))
     #p.write("%d\n" %s)
     #f.write("Computation time: priority\n")
     #p.write("%.15f\n"%np.mean(x2))
     #p.write("%.15f\n"%np.std(x2))
     #.write("Movement time:auction\n")
     #p.write("%d\n"%np.mean(y2))
#f.write("%\n"%np.std(y))
sys.stdout=open("output.txt",'w')
print("Auction: ",timecomp_a,timemove_p)
#print("Priority: ",timecomp_p,timemove_p)
print("Auction standard deviation: ",std_a)
#print("Priority standard deviation: ",std_p)
f.close()
#p.close()
