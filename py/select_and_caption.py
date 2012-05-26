#!/usr/bin/env python
'''
This file is part of the Sloan Atlas project.
Copyright 2012 David W. Hogg (NYU).

to-do:

- Plot NASA-Sloan Atlas vs RC3 on the sky and in, say, angular size.

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
    a=data.field('RA')
    b=data.field('DEC')
    y = data.field('SERSICFLUX')
    z = data.field('SERSIC_TH50')
    p50=data.field('PETROTH50')
    p90=data.field('PETROTH90')
    good=np.array([True for x in data.field('RA')])
    indx1=np.where(y[:,3] <= 0)
    good[indx1]=False
    indx2=np.where(y[:,1] <= 0)
    good[indx2]=False
    indx3=np.where(z > 158)
    good[indx3]=False
    print z[good].shape
    
    def Mag1(y):
        return 22.5-2.5*np.log10(np.abs(y))     
    def SB(y):
        return 2.5*np.log10(2*np.pi*y)
    def concentration(x,y):
    	return x/y
    	
#RAs    
x1=a[good]
badRA=a[good==False]
    
#DECs
y1=b[good]
badDec=b[good==False]
    
#i-magnitudes    
i1=Mag1(y[:,3][good])
i2=Mag1(y[:,3][indx1])
i3=Mag1(y[:,3][indx3])
    
#radii
a=z[good]
badradii=z[good==False]
    
#concentrations
c1=concentration(p90[good],p50[good])
badc=concentration(p90[good==False],p50[good==False])
    
#g & i magnitudes
i=Mag1(y[:,3][good]) #mag of positive I values
g=Mag1(y[:,1][good]) #mag of positive G values
badi=Mag1(y[:,3][good==False])
badg=Mag1(y[:,1][good==False])
    
#colors
h=g-i #all positive colors
badgi=badg-badi
	
#i-surface brightnesses       
sb=i+SB(z[good]) #i-sb from good values
badsb=badi+SB(badradii)

#scatter plot of RA vs. DEC 
fig1 = plt.figure(1)
plt.xlabel('Right Ascension')
plt.ylabel('Declination')
plt.plot(badRA,badDec,'m.',alpha=0.5)
plt.plot(x1,y1,'k.', alpha=0.5)
plt.xlim(-5,360)
plt.ylim(-30,90)
plt.savefig('RA_DEC.png')
    
#scatter plot of radii vs. magnitude calculated using i-band flux
fig2 = plt.figure(2)
plt.plot(i2,z[indx1],'m.', alpha=0.5, label='mag from negative flux')
plt.plot(i3,z[indx3],'m.', alpha=0.5, label='mag from radius > 158')
plt.plot(i1,a,'k.', alpha=0.5, label='mag from positive flux')
plt.ylabel('Half-Light Radius (arcsec)')
plt.xlabel(r"$i$ (mag)")  
plt.xlim(7,23)
plt.ylim(0,180)
plt.savefig('radius_imag.png')

#G-I color vs. radius
fig3 = plt.figure(3)
plt.plot(badgi,badradii, 'm.', alpha=0.5, label='Color from bad fluxes')
plt.plot(h,a,'k.', alpha=0.5, label='Color from +g-(+i)')
plt.xlim(0,6)
plt.ylim(0,180)
plt.xlabel(r"$g-i$ color (mag)")
plt.ylabel('Half-Light Radius (arcsec)')
plt.savefig('g_minus_i_vs_radius.png')
    
#i-magnitude vs. g-i color
fig4= plt.figure(4)
plt.plot(badi,badgi, 'm.', alpha=0.5, label='bad')
plt.plot(i,h,'k.', alpha=0.5, label='good')  
plt.xlabel(r"$i$ (mag)")
plt.ylabel(r"$g-i$ color (mag)")
plt.xlim(8,21)
plt.ylim(0,6)
plt.savefig('imag_vs_g_minus_i_color.png')
 
#i-band surface brightness vs. g-i color
fig5=plt.figure(5)
plt.plot(badsb, badgi, 'm.', alpha=0.5, label='bad sb')
plt.plot(sb, h, 'k.', alpha=0.5, label='sb of good values')
plt.ylim(0,6)
plt.xlim(16,28)
plt.xlabel(r"$i$ Surface Brightness(mag/arcsec$^2$)")
plt.ylabel(r"$g-i$ color (mag)")
plt.axhline(y=2.12026, color='r',label='2.12026')
plt.axhline(y=2.95937, color='r',label='2.95937')
plt.axhline(y=4.16176, color='r',label='4.16176')

plt.axvline(x=19.5542, ymin=0, ymax=.35338, color='r')
plt.axvline(x=20.6786, ymin=0, ymax=.35338, color='r')
plt.axvline(x=22.0141, ymin=0, ymax=.35338, color='r')

plt.axvline(x=19.0024, ymin=.35338, ymax=.49323, color='r')
plt.axvline(x=20.2374, ymin=.35338, ymax=.49323, color='r')
plt.axvline(x=22.0168, ymin=.35338, ymax=.49323, color='r')

plt.axvline(x=18.9858, ymin=.49323, ymax=.69363,color='r')
plt.axvline(x=19.993, ymin=.49323, ymax=.69363,color='r')
plt.axvline(x=21.1327, ymin=.49323, ymax=.69363,color='r')

plt.axvline(x=18.3378, ymin=.69363, ymax=6, color='r')
plt.axvline(x=19.3626, ymin=.69363, ymax=6, color='r')
plt.axvline(x=20.3118, ymin=.69363,ymax=6, color='r')
plt.savefig('i_surfacebrightness_vs_color.png')

#radius vs. radius concentration
fig6=plt.figure(6)
plt.plot(badradii,badc, 'm.',alpha=0.5, label='bad')
plt.plot(a,c1,'k.',alpha=0.5,label='good')
plt.xlabel('Half-Light Radius (arcsec)')
plt.ylabel('Concentration (p90/p50)')
plt.xlim(29,161)
plt.ylim(0,4) 
plt.savefig('radius_vs_concentration.png') 
plt.show()   

