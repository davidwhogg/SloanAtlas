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
    n=data.field('SERSIC_N')
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
radii=z[good]
badradii=z[good==False]
    
#concentrations
c=concentration(p90[good],p50[good])
badc=concentration(p90[good==False],p50[good==False])
    
#magnitudes
u=Mag1(y[:,0][good])
g=Mag1(y[:,1][good]) 
r=Mag1(y[:,2][good])
i=Mag1(y[:,3][good])
badu=Mag1(y[:,0][good==False])
badg=Mag1(y[:,1][good==False])
badr=Mag1(y[:,2][good==False])
badi=Mag1(y[:,3][good==False])
badz=Mag1(y[:,4][good==False]) 
   
#colors
gi=g-i #all positive colors
ug=u-g
gr=g-r
ri=r-i 
iz=i-Mag1(y[:,4][good]) 
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
plt.xlim(7,23)
plt.ylim(0,180)
plt.savefig('radius_imag.png')

#G-I color vs. radius
fig3 = plt.figure(3)
plt.plot(badgi,badradii, 'm.', alpha=0.5, label='Color from bad fluxes')
plt.plot(gi,radii,'k.', alpha=0.5, label='Color from +g-(+i)')
plt.xlim(0,6)
plt.ylim(0,180)
plt.xlabel(r"$g-i$ color (mag)")
plt.ylabel('Half-Light Radius (arcsec)')
plt.savefig('g_minus_i_vs_radius.png')
    
#i-magnitude vs. g-i color
fig4= plt.figure(4)
plt.plot(badi,badgi, 'm.', alpha=0.5, label='bad')
plt.plot(i,gi,'k.', alpha=0.5, label='good')  
plt.xlabel(r"$i$ (mag)")
plt.ylabel(r"$g-i$ color (mag)")
plt.xlim(8,21)
plt.ylim(0,6)
plt.savefig('imag_vs_g_minus_i_color.png')
 
#i-band surface brightness vs. g-i color
fig5=plt.figure(5)
plt.plot(badsb, badgi, 'm.', alpha=0.5, label='bad sb')
plt.plot(sb, gi, 'k.', alpha=0.5, label='sb of good values')
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
plt.plot(radii,c,'k.',alpha=0.5,label='good')
plt.xlabel('Half-Light Radius (arcsec)')
plt.ylabel('Concentration (p90/p50)')
plt.xlim(29,161)
plt.ylim(0,4) 
plt.savefig('radius_vs_concentration.png') 
 
#comparing data to blanton galaxy properties paper 2003 
fig7=plt.figure(7,figsize=(8,8))
plt.subplots_adjust(wspace=0,hspace=0)
matplotlib.rcParams['font.size'] = 10

plt.subplot(551)
plt.plot(badug,badsersic,'m.',alpha=0.5,ms=1.5)
plt.plot(ug,sersic,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,3)
plt.ylim(0.5,5.5)
plt.yticks([1,2,3,4,5],[1,2,3,4,5])
plt.xlabel(r"$u-g$")
plt.ylabel('n')

plt.subplot(552)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.plot(badgr,badsersic,'m.',alpha=0.5,ms=1.5)
plt.plot(gr,sersic,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,1.2)
plt.ylim(0.5,5.5)
plt.xlabel(r"$g-r$")

plt.subplot(553)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.plot(badri,badsersic,'m.',alpha=0.5,ms=1.5)
plt.plot(ri,sersic,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,0.6)
plt.ylim(0.5,5.5)
plt.xlabel(r"$r-i$")

plt.subplot(554)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.plot(badiz,badsersic,'k.',alpha=0.5,ms=1.5)
plt.plot(iz,sersic,'k.',alpha=0.5,ms=1.5)
plt.xlim(-0.4,0.6)
plt.ylim(0.5,5.5)
plt.xlabel(r"$i-z$")

plt.subplot(555)
plt.tick_params(axis='both',labelleft='off')
plt.plot(badsb,badsersic,'m.',alpha=0.5,ms=1.5)
plt.plot(sb,sersic,'k.',alpha=0.5,ms=1.5)
plt.xlim(17,24)
plt.xticks([18,20,22,24],[18,20,22,24])
plt.ylim(0.5,5.5)
plt.xlabel(r"$\mu_i$")

plt.subplot(556)
plt.plot(badug,badsb,'m.',alpha=0.5,ms=1.5)
plt.plot(ug,sb,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,3)
plt.ylim(17,24)
plt.yticks([18,20,22,24],[18,20,22,24])
plt.xlabel(r"$u-g$")
plt.ylabel(r"$\mu_i$")

plt.subplot(557)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.plot(badgr,badsb,'m.',alpha=0.5,ms=1.5)
plt.plot(gr,sb,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,1.2)
plt.ylim(17,24)
plt.xlabel(r"$g-r$")

plt.subplot(558)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.plot(badri,badsb,'m.',alpha=0.5,ms=1.5)
plt.plot(ri,sersic,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,0.6)
plt.ylim(17,24)
plt.xlabel(r"$r-i$")

plt.subplot(559)
plt.tick_params(axis='both',labelleft='off')
plt.plot(badiz,badsb,'k.',alpha=0.5,ms=1.5)
plt.plot(iz,sb,'k.',alpha=0.5,ms=1.5)
plt.xlim(-0.4,0.6)
plt.xticks([-0.2,0.0,0.2,0.4],[-0.2,0.0,0.2,0.4])
plt.ylim(17,24)
plt.xlabel(r"$i-z$")

plt.subplot(5,5,11)
plt.plot(badug,badiz,'m.',alpha=0.5,ms=1.5)
plt.plot(ug,iz,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,3)
plt.ylim(-0.4,0.6)
plt.yticks([-0.2,0.0,0.2,0.4],[-0.2,0.0,0.2,0.4])
plt.xlabel(r"$u-g$")
plt.ylabel(r"$i-z$")

plt.subplot(5,5,12)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.plot(badgr,badiz,'m.',alpha=0.5,ms=1.5)
plt.plot(gr,iz,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,1.2)
plt.ylim(-0.4,0.6)
plt.xlabel(r"$g-r$")

plt.subplot(5,5,13)
plt.tick_params(axis='both',labelleft='off')
plt.plot(badri,badiz,'m.',alpha=0.5,ms=1.5)
plt.plot(ri,iz,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,0.6)
plt.xticks([0.1,0.2,0.3,0.4,0.5],[0.1,0.2,0.3,0.4,0.5])
plt.ylim(-0.4,0.6)
plt.xlabel(r"$r-i$")

plt.subplot(5,5,16)
plt.plot(badug,badri,'m.',alpha=0.5,ms=1.5)
plt.plot(ug,ri,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,3)
plt.ylim(0,0.6)
plt.yticks([0.1,0.2,0.3,0.4,0.5],[0.1,0.2,0.3,0.4,0.5])
plt.xlabel(r"$u-g$")
plt.ylabel(r"$r-i$")

plt.subplot(5,5,17)
plt.tick_params(axis='both',labelleft='off')
plt.plot(badgr,badri,'m.',alpha=0.5,ms=1.5)
plt.plot(gr,ri,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,1.2)
plt.xticks([0.2,0.4,0.6,0.8,1.0],[0.2,0.4,0.6,0.8,1.0])
plt.ylim(0,0.6)
plt.xlabel(r"$g-r$")

plt.subplot(5,5,21)
plt.plot(badug,badgr,'m.',alpha=0.5,ms=1.5)
plt.plot(ug,gr,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,3)
plt.xticks([0.5,1.0,1.5,2.0,2.5],[0.5,1.0,1.5,2.0,2.5])
plt.xlabel(r"$u-g$")
plt.yticks([0.2,0.4,0.6,0.8,1.0],[0.2,0.4,0.6,0.8,1.0])
plt.ylim(0,1.2)
plt.ylabel(r"$g-r$")
plt.savefig('comparison_to_Figure_7.png')
plt.show() 