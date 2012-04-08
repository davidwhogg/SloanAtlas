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

#histogram of the 'half-light radius' distribution
fig1 = plt.figure(1)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    for t in data.field('SERSIC_TH50'):
        if t > 159: print t
    plt.clf
    plt.hist(data.field('SERSIC_TH50'))
    plt.xlabel('half-light radius (arcsec)')
    plt.savefig('radius_distribution.png')  
    
#scatter plot of RA vs. DEC 
fig2 = plt.figure(2)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    x=data.field('RA')
    y=data.field('DEC')
    plt.xlabel('Right Ascension')
    plt.ylabel('Declination')
    plt.plot(x,y,'.m')
    plt.xlim(-50,400)
    plt.title('RA vs. Dec')
    plt.savefig('RA_DEC.png')
  
#scatter plot of the radii vs. flux in the i-band
fig3 = plt.figure(3)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    y=data.field('SERSIC_TH50')
    x=data.field('SERSICFLUX')
    a=x[:,4]
    plt.ylabel('Half-light Radius (arcsec)')
    plt.xlabel('i-Flux')
    plt.title('Radius vs. i-Flux')
    plt.plot(a,y,'.c')
    plt.ylim(25, 165)  
    plt.savefig('radius_iband.png')

# Radius vs. i-Flux for positive i-Flux values only
#there are 40 negative values that are not shown here  
#3651 galaxies are plotted
fig4 = plt.figure(4)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    z=data.field('SERSIC_TH50')
    y=data.field('SERSICFLUX')
    good=np.array([True for x in data.field('RA')])
    indx=np.where(y[:,4] < 0)
    good[indx]=False
    m=z[good]
    n=y[:,4][good]
    plt.ylabel('Half-Light Radius (arcsec)')
    plt.xlabel('Flux- i band')
    plt.plot(n, m,'.c')
    plt.ylim(20,165)
    plt.xlim(-100000, 1000000)
    plt.title('Radius vs. Good Values for i-Flux')
    plt.savefig('radius_goodiflux')    
    
#distribution of G-I magnitude
#something about this data won't allow for histogram...
fig5 = plt.figure(5)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    y = data.field('SERSICFLUX')
    good=np.array([True for x in data.field('RA')])
    indx1=np.where(y[:,4] < 0)
    good[indx1]=False
    indx2=np.where(y[:,2] < 0)
    good[indx2]=False
    def Mag(y): 
        return 22.5-(2.5*np.log10(y)) 
    i=Mag(y[:,4][good])
    g=Mag(y[:,2][good])
    h=g-i
    plt.plot(h,'.r')  
    plt.xlabel('G-I Magnitude Distribution')
    plt.savefig('g_minus_i.png')

#scatter plot of radii vs. magnitude calculated using i-band flux
#magnitude originating from negative flux values are show in red
#magnitude originiated from positive values are shown in red
fig6 = plt.figure(6)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    x=data.field('SERSIC_TH50')
    y=data.field('SERSICFLUX')
    z=y[:,4]
    def iMag1(y):
        for t in y:
            t < 0 
        return 22.5-2.5*np.log10(np.abs(y))  
    def iMag2(y):
        for t in y:
            t > 0
        return 22.5-2.5*np.log10(y)
    f=iMag1(z)   
    g=iMag2(z)
    plt.plot(f,x,'.r')
    plt.plot(g,x,'.b')
    plt.ylabel('Half-Light Radius (arcsec)')
    plt.xlabel('Magnitude from i-Flux')  
    plt.title('Radius vs. I-Magnitude')
    plt.xlim(0,35)
    plt.ylim(25,165)
    plt.savefig('radius_imag.png')
 
#scatter plot of radii vs. magnitude calculated using i-band flux where only 'good' values of flux are used
#3651 galaxies
fig7 = plt.figure(7)
if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    z=data.field('SERSIC_TH50')
    y=data.field('SERSICFLUX')
    good=np.array([True for x in data.field('RA')])
    indx=np.where(y[:,4] < 0)
    good[indx]=False
    def iMag(y):
        return 22.5-2.5*np.log10(y)
    g=iMag(y[:,4][good]) 
    m=z[good]
    plt.plot(g, m ,'.b')
    plt.ylabel('Half-Light Radius (arcsec)')
    plt.xlabel('Magnitude from i-Flux') 
    plt.title('Radius vs. Good I-Magnitude')
    plt.xlim(0,35)
    plt.ylim(25,165)
    plt.savefig('radius_imag_good.png')   
    
    
plt.show()  

