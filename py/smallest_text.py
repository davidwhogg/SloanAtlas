#prints prospectus information for 16 exemplars
import matplotlib
import numpy as np
import pylab as plt
import pyfits as pyf
from yanny import *
from math import floor

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    a=data.field('RA')
    b=data.field('DEC')
    y=data.field('SERSICFLUX')
    z = data.field('SERSIC_TH50')
    w=data.field('IAUNAME')
    e=data.field('NSAID')
    f=data.field('DFLAGS')
    good=np.array([True for x in data.field('RA')])
    indx1=np.where(y[:,3] <= 0)
    good[indx1]=False
    indx2=np.where(y[:,1] <= 0)
    good[indx2]=False
    indx3=np.where(z >= 158)
    good[indx3]=False
    
nsa = read_yanny('comments.par')
comments = nsa['COMMENT']      
comment = comments['comment']
nsauser = comments['nsauser']
nsaid   = comments['nsaid']
time    = comments['time'] 


    
def Mag1(y):
    return 22.5-2.5*np.log10(np.abs(y))     
def SB(y):
    return 2.5*np.log10(2*np.pi*y)
        
#magnitudes
u=Mag1(y[:,0][good])
g=Mag1(y[:,1][good]) 
r=Mag1(y[:,2][good])
i=Mag1(y[:,3][good])
badu=Mag1(y[:,0][good==False])
badg=Mag1(y[:,1][good==False])
badr=Mag1(y[:,2][good==False])
badi=Mag1(y[:,3][good==False])
badz=Mag1(y[:,4][good==False]) 
   
#colors
gi=g-i #all positive colors
ug=u-g
gr=g-r
ri=r-i 
iz=i-Mag1(y[:,4][good]) 

badgi=badg-badi
badug=badu-badg
badgr=badg-badr
badri=badr-badi
badiz=badi-badz 



#for galaxies with comments

sixteen=[141654,162575,165451,44545,137237,129827,8756,115565,93093,76778,133790,66672,
141473,91658,136051,98900]

inds = [i for i in xrange(len(nsaid)) if nsaid[i] in sixteen]
for i in inds:	
	search=[t for t in xrange(len(e[good])) if e[good][t] ==nsaid[i]]
	for t in search:
		print 'index of atlas data set:',t
		print 'NSAID:',e[good][t]
		print 'IAU Name:', w[good][t]
		print 'RA:', a[good][t]
		print 'Dec:', b[good][t]
		print 'Radius:',z[good][t]
		print 'Dflags:',f[good][t]
		print 'colors:', ug[t], gr[t], ri[t], iz[t]
		print 'r magnitude:',r[t]	
	print 'Comment:',comment[i]
	print 'user:', nsauser[i]
	print 'time:', time[i]	
	print #space#
	
index=[t for t in xrange(len(e[good])) if e[good][t] in sixteen]
for t in index:
	print 'good index:',t, 'NSAID:', e[good][t]

#for galaxies without comments
def nocomments(x):
	print t	
	print 'NSAID:',e[good][t]
	print 'IAU Name:', w[good][t]
	print 'RA:', a[good][t]
	print 'Dec:', b[good][t]
	print 'Radius:',z[good][t]
	print 'Dflags:',f[good][t]
	print 'colors:', ug[t], gr[t], ri[t], iz[t]
	print 'r magnitude:',r[t]
	print 'Comment:NONE'
	return ''
print''

x=[76,366,807,844,957,1114,1221,1273,1297,1451,1475,1986,2023]
for t in x:
	print nocomments(x)