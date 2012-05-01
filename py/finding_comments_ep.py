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
    a=data.field('RA')
    b=data.field('DEC')
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

for theid in y[good==False]:
    inds = [i for i in xrange(len(nsaid)) if nsaid[i] == theid]

    for i in inds:
        print 'row', i
        print 'NSAID', nsaid[i]
        galaxy= [s for s in xrange(len(y)) if nsaid[i] == y[s]]
        for s in galaxy:
            print 'IAU:',w[s]
            print 'flux:',x[s]
            print 'radius:',z[s]
        print 'user:', nsauser[i]
        print 'time:', time[i]
        print 'comment:',comment[i]
        declination=[s for s in xrange(len(b)) if nsaid[i] == y[s]]
        for s in declination:
            if b[s] > 0: print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/p%s/%s/%s.jpg' % (w[s][1:3],w[s][11:13],w[s],w[s])
            else: print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/m%s/%s/%s.jpg' % (w[s][1:3],w[s][11:13],w[s],w[s])
            print #space#

nocom = [t for t in xrange(len(y[good==False])) if y[good==False][t] not in nsaid]
for t in nocom:    
    print 'NSAID',y[t]
    print 'IAU:',w[t]
    print 'flux:',x[t]
    print 'radius:',z[t]
    print 'comment: NONE '
    #declination=[t for t in xrange(len(b)) if y[t] not in nsaid]
    #for t in declination:
    if b[t] > 0: print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/p%s/%s/%s.jpg' % (w[t][1:3],w[t][11:13],w[t],w[t])
    else: print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/m%s/%s/%s.jpg' % (w[t][1:3],w[t][11:13],w[t],w[t])
    print #space#

#25268,29809-nsaid--uses the integer before the dec value given in IAU name, its when the following two numbers are 00
#nsaid 32995- J123454.85+512330.8 uses 50 instead of 51

    

    
        

    
    
 

#u g r i z
    