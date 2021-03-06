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
    c=data.field('PID')
    good=np.array([True for a in data.field('RA')])
    indx1=np.where(x[:,3] <= 0)
    indx2=np.where(x[:,1] <= 0)
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
            if b[s] > 0: 
            	print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/p%02d/%s/%s.jpg' % (w[s][1:3],(int(w[s][11:13])/2)*2,w[s],w[s])
            	print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/p%02d/%s/atlases/%s/' % (w[s][1:3],(int(w[s][11:13])/2)*2,w[s],c[s])
            else: 
            	print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/m%02d/%s/%s.jpg' % (w[s][1:3],(int(w[s][11:13])/2)*2,w[s],w[s])
                print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/m%02d/%s/atlases/%s/' % (w[s][1:3],(int(w[s][11:13])/2)*2,w[s],c[s])
        print #space#																						
       		
nocom = [t for t in xrange(len(y[good==False])) if y[good==False][t] not in nsaid]
for t in nocom:    
	print 'NSAID',y[good==False][t]
	print 'IAU:',w[good==False][t]
	print 'flux:',x[good==False][t]
	print 'radius:',z[good==False][t]
	print 'comment: NONE '    
	if b[good==False][t] > 0: 
    		print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/p%02d/%s/%s.jpg' % (w[good==False][t][1:3],(int(w[good==False][t][11:13])/2)*2,w[good==False][t],w[good==False][t])
    		print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/p%02d/%s/atlases/%s/' % (w[good==False][t][1:3],(int(w[good==False][t][11:13])/2)*2,w[good==False][t],c[good==False][t])
	
	else: 
			print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/m%02d/%s/%s.jpg' % (w[good==False][t][1:3],(int(w[good==False][t][11:13])/2)*2,w[good==False][t],w[good==False][t])
			print 'http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/m%02d/%s/atlases/%s/' % (w[good==False][t][1:3],(int(w[good==False][t][11:13])/2)*2,w[good==False][t],c[good==False][t])
	print #space#



    

    
        

    
    
 

#u g r i z
    