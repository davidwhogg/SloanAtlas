#!/usr/bin/env python
'''
This file is part of the Sloan Atlas project.
Copyright 2012 David W. Hogg (NYU).

to-do:

- Make plots of the input catalog (currently the NASA-Sloan Atlas) to
  guide selection.

- Design boxels in top-level space (color and central surface
  brightness?).

- Within each boxel, select galaxies in decreasing order in angular
  size.

- For each galaxy selected, produce "caption information" including
  plots of location in property space (say, radial profile and
  something?), RC3 classification, and GalaxyZoo information.

- Build plates from galaxies based on angular size and build joint
  captions for plates.
'''

import matplotlib
#matplotlib.use('Agg')
#from matplotlib import rc
#rc('font',**{'family':'serif','serif':'Computer Modern Roman','size':12})
#rc('text', usetex=True)
import numpy as np
import pylab as plt
import pyfits as pyf


fig1 = plt.figure(1)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    for t in data.field('SERSIC_TH50'):
        if t > 159: print t
    plt.clf
    plt.hist(data.field('SERSIC_TH50'))
    plt.xlabel('half-light radius (arcsec)')
    plt.savefig('radius_distribution.png')    
 
fig2 = plt.figure(2)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    x=data.field('RA')
    y=data.field('DEC')
    plt.xlabel('Right Ascension')
    plt.ylabel('Declination')
    plt.plot(x,y,'.m')
    plt.xlim(-50,400)
    plt.savefig('RA_DEC.png')
      
  

fig3 = plt.figure(3)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    x=data.field('SERSIC_TH50')
    y=data.field('SERSICFLUX')
    def iFlux(y):
        for t in y:
            i=t[5]
        return y    
    plt.ylabel('half-light radius (arcsec)')
    plt.xlabel('Flux- i band')
    plt.plot(y,x,'.c')
    plt.ylim(30, 165)  
    plt.savefig('radius_iband.png')
  
fig4 = plt.figure(4)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    x=data.field('SERSIC_TH50')
    y=data.field('SERSICFLUX')
    def iMag1(y):
        for t in y:
            t[5] < 0 
        return 22.5-2.5*np.log10(np.abs(y))  
    def iMag2(y):
        for t in y:
            t[5] > 0
        return 22.5-2.5*np.log10(y)
    f=iMag1(y)   
    g=iMag2(y)
    plt.plot(f,x,'.r')
    plt.plot(g,x,'.b')
    plt.ylabel('half-light radius (arcsec)')
    plt.xlabel('Magnitude- i band')    
    plt.xlim(-20,140)
    plt.ylim(20,165)
    plt.savefig('radius_magiband.png')
plt.show()  

