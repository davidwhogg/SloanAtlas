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


if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    for t in data.field('SERSIC_TH50'):
        if t > 159: print t
    plt.clf
    plt.hist(data.field('SERSIC_TH50'))
    plt.xlabel('half-light radius (arcsec)')
    plt.savefig('radius_distribution.png')    
plt.show()  

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    x=data.field('RA')
    y=data.field('DEC')
    plt.xlabel('Right Ascension')
    plt.ylabel('Declination')
    plt.plot(x,y,'.m')
    plt.savefig('RA_DEC.png')
    plt.xlim(-50,400)
      
plt.show()  


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
    plt.savefig('radius_iband.png')
    plt.ylim(30, 165)     
plt.show()   

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    x=data.field('SERSIC_TH50')
    y=data.field('SERSICFLUX')
    def iMag(y):
        for t in y:
            g=t[5]
        return 22.5-2.5*np.log10(np.abs(y))   
    f=iMag(y)
    plt.ylabel('half-light radius (arcsec)')
    plt.xlabel('Magnitude- i band')
    plt.plot(f,x,'.b')
    plt.savefig('radius_magiband.png')    
    plt.xlim(-20,140)
    plt.ylim(20,165) 
plt.show()  

