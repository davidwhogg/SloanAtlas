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
    good=np.array([True for x in data.field('RA')])
    indx1=np.where(y[:,4] < 0)
    good[indx1]=False
    indx2=np.where(y[:,2] < 0)
    good[indx2]=False
    indx3=np.where(z > 158)
    good[indx3]=False
    
    def Mag1(y):
        return 22.5-2.5*np.log10(np.abs(y))  
    def Mag2(y):
        return 22.5-2.5*np.log10(y)    
    def SB(y):
        return 2.5*np.log10(2*np.pi*y)
    #RAs    
    x1=a[good]
    x2=a[indx1]
    x3=a[indx2]
    x4=a[indx3]
    
    #DECs
    y1=b[good]
    y2=b[indx1]
    y3=b[indx2]
    y4=b[indx3]
    
    #i-magnitudes    
    i1=Mag2(y[:,4][good])
    i2=Mag1(y[:,4][indx1])
    i3=Mag1(y[:,4][indx3])
    
    #radii
    a=z[good]
    b=z[indx1]
    c=z[indx2]
    d=z[indx3]
    
    #g & i magnitudes
    i=Mag1(y[:,4][good]) #mag of positive I values
    g=Mag1(y[:,2][good]) #mag of positive G values
    j=Mag1(y[:,4][indx1]) #mag of negative I values
    k=Mag1(y[:,2][indx2]) #mag of negative G values 
    l=Mag1(y[:,4][indx2]) #mag of I values corresponding to neg G values
    m=Mag1(y[:,2][indx1]) #mag of G values corresponding to neg I values
    p=Mag1(y[:,4][indx3]) # mag of I values that correspond to r > 158 
    q=Mag1(y[:,2][indx3]) # mag of G values that correspond to r > 158
    
    #colors
    h=g-i #all positive colors
    n=m-j #+G-(-I)
    o=k-l #-G-(+I)
    r=q-p # bad colors from r > 158 
    
    #i-surface brightnesses       
    sb=i+SB(z[good]) #i-sb from good values
    sb1=p+SB(z[indx3]) #i-sb from bad r values
    sb2=j+SB(z[indx1])#i-sb from negative i values 
    sb3=l+SB(z[indx2])#i-sb from negative g values
    
#scatter plot of RA vs. DEC 
fig1 = plt.figure(1)
plt.xlabel('Right Ascension')
plt.ylabel('Declination')
plt.plot(x2, y2, 'm.', alpha=0.5)
plt.plot(x3,y3,'m.',alpha=0.5)
plt.plot(x4,y4,'m.',alpha=0.5)
plt.plot(x1,y1,'k.', alpha=0.5)
plt.xlim(-5,360)
plt.ylim(-30,90)
plt.savefig('RA_DEC.png')
    
#scatter plot of radii vs. magnitude calculated using i-band flux
fig2 = plt.figure(2)
plt.plot(i2,b,'m.', alpha=0.5, label='mag from negative flux')
plt.plot(i3,d,'m.', alpha=0.5, label='mag from radius > 158')
plt.plot(i1,a,'k.', alpha=0.5, label='mag from positive flux')
plt.ylabel('Half-Light Radius (arcsec)')
plt.xlabel(r"$i$ (mag)")  
plt.xlim(7,23)
plt.ylim(0,180)
plt.savefig('radius_imag.png')

#G-I magnitude vs. radius
fig3 = plt.figure(3)
plt.plot(n,b, 'm.', alpha=0.5, label='Mag from +g-(-i)')
plt.plot(o,c, 'm.', alpha=0.5, label='Mag from -g-(+i)')
plt.plot(r, d, 'm.', alpha=0.5, label='Mag from r > 158')
plt.plot(h,a,'k.', alpha=0.5, label='Mag from +g-(+i)')
plt.xlim(0,4)
plt.ylim(0,180)
plt.xlabel(r"$g-i$ color (mag)")
plt.ylabel('Half-Light Radius (arcsec)')
plt.savefig('g_minus_i_vs_radius.png')
    
#i-magnitude vs. g-i color
fig4= plt.figure(4)
plt.plot(p,r, 'm.', alpha=0.5, label='Mag from r >158')
plt.plot(j,n, 'm.', alpha=0.5, label='Mag from +g-(-i)')
plt.plot(l,o, 'm.', alpha=0.5, label='Mag from -g-(+i)')
plt.plot(i,h,'k.', alpha=0.5, label='Mag from +g-(+i)')  
plt.xlabel(r"$i$ (mag)")
plt.ylabel(r"$g-i$ color (mag)")
plt.xlim(6,21)
plt.ylim(0,4)
plt.legend()
plt.savefig('imag_vs_g_minus_i_color.png')
 
#i-band surface brightness vs. g-i color
fig5=plt.figure(5)
plt.plot(sb1, r, 'm.', alpha=0.5, label='sb of r > 158')
plt.plot(sb2,n,'m.',alpha=0.5, label='sb of neg i-flux')
plt.plot(sb3, o, 'm.', alpha=0.5, label='sb of neg g-flux')
plt.plot(sb, h, 'k.', alpha=0.5, label='sb of good values')
plt.ylim(0,4)
plt.xlim(14,27)
plt.xlabel(r"$i$ Surface Brightness(mag/arcsec$^2$)")
plt.ylabel(r"$g-i$ color (mag)")
plt.savefig('i_surfacebrightness_vs_color.png')
    
plt.show()   

