'''
Created on Sep 4, 2014

@author: mueller
'''
import pandas as pd
import numpy as np
import pandas.io.sql as psql
from sqlalchemy import  create_engine

# import MySQLdb
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib import rcParams
import re
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
engine=create_engine("mysql+mysqlconnector://root:admin@localhost/floatbook")
rcParams.update({'figure.autolayout':True})
#conn=mysql.connector.connect(user = 'root', password = 'admin', host = '127.0.0.1', database='floatbook')
sql="SELECT * from vtest3 where COLUMN_NAME like '%C%\_bid' or COLUMN_NAME like '%C%\_ask' or COLUMN_NAME like '%P%\_bid' or COLUMN_NAME like '%P%\_ask'"
pd.set_option('display.max_columns',300) 
pd.set_option('display.max_rows',300)
#df=psql.frame_query(sql,con=conn) 
df=pd.read_sql_query(sql,engine)
sql14=""
for i in df.index:
    if i==0:
        sql14=df['COLUMN_NAME'][i]
    else:
        sql14=sql14+", "+df['COLUMN_NAME'][i]
      
sql22="SELECT "+sql14+" from mo140118351"
#ba=psql.frame_query(sql22,con=conn)
ba=pd.read_sql_query(sql22,engine)
# re.findall(r'\d+',x)[1]
z=list()
for i in df.index:
   x=df['COLUMN_NAME'][i]
# use regular expressions, find sets of one or more digits; save the second set
   y=re.findall(r'\d+',x)[1]                         
   z.append(y)

# remove duplicates - a set removes duplicates, converterd back to list afterwards
aa=list(set(z))
aa.sort()
# aa is now my list of strikes
ab=[float(i) for i in aa]
# ab is now a float list of strikes (to do math)
ac=list(enumerate(ab))
# ac now has an index for the associated values of ab strikes; each new set starts at 4*index
print ('Strikes:') 
print (aa)
print ('Bids & asks: "')
print (df)
scbh=ba.iloc[:,37]
bpah=ba.iloc[:,39]
spbl=ba.iloc[:,34]
bcal=ba.iloc[:,32]
float3=(ab[9]-ab[8])+spbl+scbh-(bpah+bcal)
# here we have the following:
# high strike - index 9; high strike set - starts at 9*4=36, 
# goes in order call_ask, call_bid, put_bit, put_ask (indices 36,37,38,39)
# low strike - index 8; low strike set - starts at 8*4=32, goes in order call_ask, call_bid, put_bit, put_ask (indices 32, 33, 34, 35)


xx=list()
ss=list()

# spbl_ind= strike index*4+2
# bcal_ind= strike index*4

# for i,j in ac:
#   ss_ind=i*4+1
#   xx=ba.iloc[:,ss_ind]
#   ss.append(xx)
#   print ss
bpah=list()
scbh=list()
spbl=list()
bcal=list()
scbl=list()
spbh=list()
bpal=list()
bcah=list()

float_strikes=list()
float_debits=list()
float_credits=list()
strike_combo=list()
for x,y in ac:
   spbl_ind=x*4+2
   bcal_ind=x*4
   bpal_ind=x*4+3
   scbl_ind=x*4+1
   low_strike_ind=x
   for i,j in ac:
      if i<x:
         next
      else:
         bpah_ind=i*4+3
         scbh_ind=i*4+1
         bcah_ind=i*4
         spbh_ind=i*4+2
#      spbl_ind=8*4+2
#      bcal_ind=8*4
         high_strike_ind=i
         bpah=ba.iloc[:,bpah_ind]
         scbh=ba.iloc[:,scbh_ind]
         spbl=ba.iloc[:,spbl_ind]
         bcal=ba.iloc[:,bcal_ind]
         scbl=ba.iloc[:,scbl_ind]
         spbh=ba.iloc[:,spbh_ind]
         bpal=ba.iloc[:,bpal_ind]
         bcah=ba.iloc[:,bcah_ind]
         float_debit=(ab[high_strike_ind]-ab[low_strike_ind])-(bpah+bcal)+(scbh+spbl)
         float_credit=(scbl+spbh)-(bpal+bcah)-(ab[high_strike_ind]-ab[low_strike_ind])
         float_debits.append(float_debit)
         float_credits.append(float_credit)
         float_strike="%d-%d" % (ab[low_strike_ind],ab[high_strike_ind])
         float_strikes.append(float_strike)
  # bpah.append(xx)
  # scbh.append(yy)
   
# spbl=ba.iloc[:,spbl_ind]
# bcal=ba.iloc[:,bcal_ind]


#Credit position:
#FLOAT= (scbl+spbh) - (bpal + bcah)  - (high_strike-low_strike)

#Debit position:
#FLOAT= (high_strike-low_strike) - (bpah+bcal) + (scbh+spbl)



from numpy import *
cc=array(float_debits)
ff=array(float_credits)

from pandas import *
dd=DataFrame(cc)
gg=DataFrame(ff)
ee=dd.T
hh=gg.T

print("Low strike is: %f and high strike is %f" % (ab[low_strike_ind],ab[high_strike_ind]))
qq="%d-%d" % (ab[low_strike_ind],ab[high_strike_ind])
vv=array(float_strikes)
ee.columns=vv
hh.columns=vv

# Generating float table for graphing
#begin=0
#c_range_max=int(ab[15])
#c_range_min=int(ab[0])-1
#float_graph=pd.DataFrame()
#j=0
#for i in range(16,0,-1):
   
   #begin_next=begin+i
   #print begin, begin_next, i
   
   #float_graph1=ee.iloc[0:1,begin:begin_next]
   #float_graph1=float_graph1.sort_index(axis=1, ascending=False)
   #float_graph1.columns=range(c_range_max,c_range_min+j,-1)
   #float_graph=float_graph.append(float_graph1)
   #j=j+1
   #begin=begin_next
#float_graph.index=range(int(ab[0]),int(ab[15])+1)   
#float_graph=float_graph.sort_index(axis=0, ascending=False)


#fig = plt.figure()
#ax=fig.gca(projection='3d')
#x=float_graph.index
#y=float_graph.columns
#z=float_graph.values
#z=np.nan_to_num(z)
#x,y=meshgrid(x,y)
#surf = ax.plot_surface(x,y,z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=1, antialiased=False)
#plt.title("FLOAT Slice")
#plt.savefig("FLOAT_slice.png", transparent=True)
#plt.show()


#--- first subplot
fig = plt.figure(figsize=(7,10))
ax1 = fig.add_subplot(211, projection='3d')
ax1.grid(False)
ax2 = fig.add_subplot(212, projection='3d')
ax2.grid(False)


def init():
   wframe=ax.plot_wireframe([],[],[],rstride=2, cstride=2)
   return wframe
   
def float_anim(i):
 
   
      begin=0
      c_range_max=int(ab[15])
      c_range_min=int(ab[0])-1
      debit_graph=pd.DataFrame()
      credit_graph=pd.DataFrame()
      j=0
      for k in range(16,0,-1):
    
         begin_next=begin+k
         # print begin, begin_next, i
     
         float_graph_debit=ee.iloc[i:i+1,begin:begin_next]
         float_graph_credit=hh.iloc[i:i+1,begin:begin_next]
         
         float_graph_debit=float_graph_debit.sort_index(axis=1, ascending=True)
         float_graph_credit=float_graph_credit.sort_index(axis=1, ascending=True)
         
         float_graph_debit.columns=range(c_range_max,c_range_min+j,-1)
         float_graph_credit.columns=range(c_range_max,c_range_min+j,-1)
         
         debit_graph=debit_graph.append(float_graph_debit)
         credit_graph=credit_graph.append(float_graph_credit)
         j=j+1
         begin=begin_next
           
      debit_graph.index=range(int(ab[0]),int(ab[15])+1) 
      credit_graph.index=range(int(ab[0]),int(ab[15])+1)
      
      debit_graph=debit_graph.sort_index(axis=0, ascending=True)
      credit_graph=credit_graph.sort_index(axis=0, ascending=True)
 
      x=debit_graph.index
      y=debit_graph.columns
      z=debit_graph.values
      z=np.nan_to_num(z)
      x,y=meshgrid(x,y)
      ax2.clear()
      ax2.grid(False)
      ax2.set_zlim3d([-2, 1])
      ax2.set_title("Debit Position")
      surf2 = ax2.plot_surface(x,y,z, rstride=1, cstride=1, cmap='RdYlGn', linewidth=0, antialiased=False)
      
      xx=credit_graph.index
      yy=credit_graph.columns
      zz=credit_graph.values
      zz=np.nan_to_num(zz)
      xx,yy=meshgrid(xx,yy)
      ax1.clear()
      ax1.grid(False)
      ax1.set_zlim3d([-2, 1])
      ax1.set_title("Credit Position")
      surf1=ax1.plot_surface(xx,yy,zz,rstride=1,cstride=1,cmap='RdYlGn', linewidth=0, antialiased=False)
      #wframe=ax.plot_wireframe(x,y,z,rstride=2, cstride=2)
      
      return surf1, surf2

# call the animator.  blit=True means only re-draw the parts that have changed.
ax1.view_init(elev=34, azim=-140)
ax2.view_init(elev=34, azim=-140)

anim = animation.FuncAnimation(fig, float_anim, frames=1500, interval=1, blit=False)



# save the animation as an mp4.  This requires ffmpeg or mencoder to be
# installed.  The extra_args ensure that the x264 codec is used, so that
# the video can be embedded in html5.  You may need to adjust this for
# your system: for more information, see
# http://matplotlib.sourceforge.net/api/animation_api.html
# anim.save('float_anim.mp4', fps=30, extra_args=['-codec:v', 'libx264'])
# anim.save('float_anim.mp4',fps=30)

plt.show()