import matplotlib
import numpy as np
import pylab as plt
import pyfits as pyf
import yanny as yanny
from yanny import *

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    y=data.field('NSAID')
    x=data.field('SERSICFLUX')
    z=data.field('SERSIC_TH50')
    w=data.field('IAUNAME')
    good=np.array([True for a in data.field('RA')])
    indx1=np.where(x[:,2] < 0)
    indx2=np.where(x[:,4] < 0)
    indx3=np.where(z > 158)
    good[indx1]=False
    good[indx2]=False
    good[indx3]=False

nsa = read_yanny('comments.par')

comments = nsa['COMMENT']
       
comment = comments['comment']
nsauser = comments['nsauser']
nsaid   = comments['nsaid']
time    = comments['time']  

theid = y
print y[good==False]
print w[good==False]
print x[good==False]
print z[good==False]
for theid in y[good==False]:
    inds = [i for i in xrange(len(nsaid)) if nsaid[i] == theid]
    print 'inds', inds
    for i in inds:
         print '  row', i, nsaid[i], time[i], nsauser[i], comment[i]


    
        

   
    
    
 

#u g r i z
    