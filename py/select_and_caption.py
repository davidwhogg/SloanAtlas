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
    def Mag2(y):
        return 22.5-2.5*np.log10(y)    
    def SB(y):
        return 2.5*np.log10(2*np.pi*y)
    def concentration(x,y):
    	return x/y
    	
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
    i1=Mag2(y[:,3][good])
    i2=Mag1(y[:,3][indx1])
    i3=Mag1(y[:,3][indx3])
    
    #radii
    a=z[good]
    b=z[indx1]
    c=z[indx2]
    d=z[indx3]
    
    #concentrations
    c1=concentration(p90[good],p50[good])
    c2=concentration(p90[indx1],p50[indx1])
    c3=concentration(p90[indx2],p50[indx2])
    c4=concentration(p90[indx3],p50[indx3])
    
    #g & i magnitudes
    i=Mag1(y[:,3][good]) #mag of positive I values
    g=Mag1(y[:,1][good]) #mag of positive G values
    j=Mag1(y[:,3][indx1]) #mag of negative I values
    k=Mag1(y[:,1][indx2]) #mag of negative G values 
    l=Mag1(y[:,3][indx2]) #mag of I values corresponding to neg G values
    m=Mag1(y[:,1][indx1]) #mag of G values corresponding to neg I values
    p=Mag1(y[:,3][indx3]) # mag of I values that correspond to r > 158 
    q=Mag1(y[:,1][indx3]) # mag of G values that correspond to r > 158
    
	#colors
	h=g-i #all positive colors
	n1=m-j #+G-(-I)
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

#G-I color vs. radius
fig3 = plt.figure(3)
plt.plot(n1,b, 'm.', alpha=0.5, label='Mag from +g-(-i)')
plt.plot(o,c, 'm.', alpha=0.5, label='Mag from -g-(+i)')
plt.plot(r, d, 'm.', alpha=0.5, label='Mag from r > 158')
plt.plot(h,a,'k.', alpha=0.5, label='Mag from +g-(+i)')
plt.xlim(0,6)
plt.ylim(0,180)
plt.xlabel(r"$g-i$ color (mag)")
plt.ylabel('Half-Light Radius (arcsec)')
plt.savefig('g_minus_i_vs_radius.png')
    
#i-magnitude vs. g-i color
fig4= plt.figure(4)
plt.plot(p,r, 'm.', alpha=0.5, label='Mag from r >158')
plt.plot(j,n1, 'm.', alpha=0.5, label='Mag from +g-(-i)')
plt.plot(l,o, 'm.', alpha=0.5, label='Mag from -g-(+i)')
plt.plot(i,h,'k.', alpha=0.5, label='Mag from +g-(+i)')  
plt.xlabel(r"$i$ (mag)")
plt.ylabel(r"$g-i$ color (mag)")
plt.xlim(8,21)
plt.ylim(0,6)
plt.legend()
plt.savefig('imag_vs_g_minus_i_color.png')
 
#i-band surface brightness vs. g-i color
fig5=plt.figure(5)
plt.plot(sb1, r, 'm.', alpha=0.5, label='sb of r > 158')
plt.plot(sb2,n1,'m.',alpha=0.5, label='sb of neg i-flux')
plt.plot(sb3, o, 'm.', alpha=0.5, label='sb of neg g-flux')
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
plt.plot(a,c1,'k.',alpha=0.5, label='concentration from good values')
plt.plot(b,c2,'m.',alpha=0.5,label='concentration from neg i-flux')
plt.plot(c,c3,'m.', alpha=0.5, label='concentration from neg g-flux')
plt.plot(d,c4, 'm.', alpha=0.5, label='concentration from r > 158')
plt.xlabel('Half-Light Radius (arcsec)')
plt.ylabel('Concentration (p90/p50)')
plt.xlim(29,161)
plt.ylim(0,4)   
plt.savefig('radius_vs_concentration.png') 
plt.show()   

