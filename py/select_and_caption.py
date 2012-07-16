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
from math import floor

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    a=data.field('RA')
    b=data.field('DEC')
    y = data.field('SERSICFLUX')
    z = data.field('SERSIC_TH50')
    n=data.field('SERSIC_N')
    p50=data.field('PETROTH50')
    p90=data.field('PETROTH90')
    good=np.array([True for x in data.field('RA')])
    indx1=np.where(y[:,5] <= 0)
    good[indx1]=False
    indx2=np.where(y[:,3] <= 0)
    good[indx2]=False
    indx3=np.where(z > 158)
    good[indx3]=False
    
    def Mag1(y):
        return 22.5-2.5*np.log10(np.abs(y))     
    def SB(y):
        return 2.5*np.log10(2*np.pi*y)
    def concentration(x,y):
    	return x/y
    def quantile(x,q):
   		sorted(x)
		i=len(sorted(x))*q
		return floor(i) 
    	
#RAs    
x1=a[good]
badRA=a[good==False]
    
#DECs
y1=b[good]
badDec=b[good==False]
    
#i-magnitudes    
i1=Mag1(y[:,5][good])
i2=Mag1(y[:,5][indx1])
i3=Mag1(y[:,5][indx3])
    
#radii
radii=z[good]
badradii=z[good==False]
    
#concentrations
c=concentration(p90[good],p50[good])
badc=concentration(p90[good==False],p50[good==False])
    
#magnitudes
u=Mag1(y[:,2][good])
g=Mag1(y[:,3][good]) 
r=Mag1(y[:,4][good])
i=Mag1(y[:,5][good])
badu=Mag1(y[:,2][good==False])
badg=Mag1(y[:,3][good==False])
badr=Mag1(y[:,4][good==False])
badi=Mag1(y[:,5][good==False])
badz=Mag1(y[:,6][good==False]) 
   
#colors
gi=g-i #all positive colors
ug=u-g
gr=g-r
ri=r-i 
iz=i-Mag1(y[:,6][good]) 
badgi=badg-badi
badug=badu-badg
badgr=badg-badr
badri=badr-badi
badiz=badi-badz 

#i-surface brightnesses       
sb=i+SB(z[good])
badsb=badi+SB(badradii)

#sersic index
sersic=n[good]
badsersic=n[good==False]

print quantile(gi,0.25)
print quantile(gi,0.5)
print quantile(gi,0.75)
color=sorted(gi)
print color[655]
print color[1310]
print color[1965]

print 'color sample = 0'
color_sample_0=[t for t in xrange(len(gi)) if gi[t] < color[655] ]

    	
print 'color sample = 1'
color_sample_1=[t for t in xrange(len(gi)) if color[655] < gi[t] < color[1310]]

    	
print 'color sample = 2' 
color_sample_2=[t for t in xrange(len(gi)) if color[1310] < gi[t] < color[1965]]

    	
print 'color sample = 3'
color_sample_3=[t for t in xrange(len(gi)) if gi[t] > color[1965]]

brightness0=sorted(sb[color_sample_0])
brightness1=sorted(sb[color_sample_1])
brightness2=sorted(sb[color_sample_2])
brightness3=sorted(sb[color_sample_3])
print quantile (brightness0,0.25)
print quantile (brightness0, 0.50)
print quantile (brightness0, 0.75)

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
plt.plot(i1,radii,'k.', alpha=0.5, label='mag from positive flux')
plt.ylabel('Half-Light Radius (arcsec)')
plt.xlabel(r"$i$ (mag)")  
plt.xlim(9,17)
plt.ylim(20,180)
plt.savefig('radius_imag.png')

#G-I color vs. radius
fig3 = plt.figure(3)
plt.plot(badgi,badradii, 'm.', alpha=0.5, label='Color from bad fluxes')
plt.plot(gi,radii,'k.', alpha=0.5, label='Color from +g-(+i)')
plt.xlim(0,2)
plt.ylim(20,180)
plt.xlabel(r"$g-i$ color (mag)")
plt.ylabel('Half-Light Radius (arcsec)')
plt.savefig('g_minus_i_vs_radius.png')
    
#i-magnitude vs. g-i color
fig4= plt.figure(4)
plt.plot(badi,badgi, 'm.', alpha=0.5, label='bad')
plt.plot(i,gi,'k.', alpha=0.5, label='good')  
plt.xlabel(r"$i$ (mag)")
plt.ylabel(r"$g-i$ color (mag)")
plt.xlim(9,17)
plt.ylim(0,2)
plt.savefig('imag_vs_g_minus_i_color.png')
 
#i-band surface brightness vs. g-i color
fig5=plt.figure(5)
plt.plot(badsb, badgi, 'm.', alpha=0.5, label='bad sb')
plt.plot(sb, gi, 'k.', alpha=0.5, label='sb of good values')
plt.ylim(0,2)
plt.xlim(16,24)
plt.xlabel(r"$i$ Surface Brightness(mag/arcsec$^2$)")
plt.ylabel(r"$g-i$ color (mag)")
plt.axhline(y=color[655], color='r')
plt.axhline(y=color[1310], color='r')
plt.axhline(y=color[1965], color='r')

plt.axvline(x=brightness0[163], ymin=0, ymax=color[655]/2, color='r')
plt.axvline(x=brightness0[327], ymin=0, ymax=color[655]/2, color='r')
plt.axvline(x=brightness0[491], ymin=0, ymax=color[655]/2, color='r')

plt.axvline(x=brightness1[163], ymin=color[655]/2, ymax=color[1310]/2, color='r')
plt.axvline(x=brightness1[327], ymin=color[655]/2, ymax=color[1310]/2, color='r')
plt.axvline(x=brightness1[491], ymin=color[655]/2, ymax=color[1310]/2, color='r')

plt.axvline(x=brightness2[163], ymin=color[1310]/2, ymax=color[1965]/2, color='r')
plt.axvline(x=brightness2[327], ymin=color[1310]/2, ymax=color[1965]/2, color='r')
plt.axvline(x=brightness2[491], ymin=color[1310]/2, ymax=color[1965]/2, color='r')

plt.axvline(x=brightness3[163], ymin=color[1965]/2, ymax=2, color='r')
plt.axvline(x=brightness3[327], ymin=color[1965]/2, ymax=2, color='r')
plt.axvline(x=brightness3[491], ymin=color[1965]/2, ymax=2, color='r')
plt.savefig('i_surfacebrightness_vs_color.png')

#radius vs. radius concentration
fig6=plt.figure(6)
plt.plot(badradii,badc, 'm.',alpha=0.5, label='bad')
plt.plot(radii,c,'k.',alpha=0.5,label='good')
plt.xlabel('Half-Light Radius (arcsec)')
plt.ylabel('Concentration (p90/p50)')
plt.xlim(29,161)
plt.ylim(0,4) 
plt.savefig('radius_vs_concentration.png') 


plt.show()