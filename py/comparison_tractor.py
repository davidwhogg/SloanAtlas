from astrometry.util.file import *
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pylab as plt
import pyfits as pyf
from astropysics.obstools import *
import operator
import math
import os
import random
from random import choice
import itertools

if __name__ == '__main__':
    data = pyf.open("nsa-short.fits.gz")[1].data
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
        return 22.5-2.5*np.log10(np.abs(y))     #input flux
    def SB(y):
        return 2.5*np.log10(2*np.pi*y) #input half-light radius
    def concentration(x,y):
    	return x/y
    def flux2mag(x):
        return 22.5-2.5*np.log10(np.abs(x))  
    def mag2flux(x):
	return 10**((x-22.5)/-2.5)

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

#UNPICKLE STARTS HERE
#4649 has bad results
ngcs=[4621,3351,4192,4548,221,3368,4254,4594,3992,4501,4374,3877,3801,3630,2654,5422]
plt.figure(figsize=(8,8))

ug_colors=[]
gr_colors=[]
ri_colors=[]
iz_colors=[]
ratios=[]
ratios2=[]
dev_mags=[]
exp_mags=[]

for ngc in ngcs:
    print ngc
    CG=unpickle_from_file('ngc-%s.pickle'%(ngc)) 
    tot=CG.getBrightness()
    print tot
    pos=CG.getPosition()
    print pos
    dev=CG.brightnessDev
    exp = CG.brightnessExp

#extinction values by filter for Sloan
    sloanu=5.155
    sloang=3.793
    sloanr=2.751
    sloani=2.086
    sloanz=1.479
#ugriz
#01234
#get extinction from SFD
    x=get_SFD_dust(pos[0], pos[1],dustmap='ebv',interpolate=True)
    correction=[x*sloanu,x*sloang,x*sloanr,x*sloani,x*sloanz]
    corrected_mags=map(operator.sub,tot,correction)
    corrected_dev=map(operator.sub,dev,correction)
    corrected_exp=map(operator.sub,exp,correction)
    
    print 'dev', dev[3],corrected_dev[3]
    print'exp', exp[3], corrected_exp[3]

#   original tractor colors
    tracug=tot[0]-tot[1]
    tracgr=tot[1]-tot[2]
    tracri=tot[2]-tot[3]
    traciz=tot[3]-tot[4]

#corrected mags
    dev_mags.append(corrected_dev[3])
    exp_mags.append(corrected_exp[3])

#corected colors
    ug_corrected=corrected_mags[0]-corrected_mags[1]
    ug_colors.append(ug_corrected)

    gr_corrected=corrected_mags[1]-corrected_mags[2]
    gr_colors.append(gr_corrected)

    ri_corrected=corrected_mags[2]-corrected_mags[3]
    ri_colors.append(ri_corrected)

    iz_corrected=corrected_mags[3]-corrected_mags[4]
    iz_colors.append(iz_corrected)

#flux ratio
    top=mag2flux(dev[3])
    bottom=(mag2flux(dev[3])+mag2flux(exp[3])) 
    print 'fr1',top,bottom
    fluxratio=top/bottom
    ratios.append(fluxratio)

print ug_colors,gr_colors,ri_colors,iz_colors
print'ratios', ratios
print dev_mags
print exp_mags

plt.subplots_adjust(wspace=0,hspace=0)
matplotlib.rcParams['font.size'] = 9

# plt.subplot(551)
# plt.xlabel(r"$u-g$")
# plt.ylabel(r'$R_f(r)$')

# plt.subplot(552)
# plt.tick_params(axis='both',labelbottom='off',labelleft='off')
# plt.xlabel(r"$g-r$")

# plt.subplot(553)
# plt.tick_params(axis='both',labelbottom='off',labelleft='off')
# plt.xlabel(r"$r-i$")
# plt.plot(ri_corrected,fluxratio(dev[2],exp[2]),'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none'

# plt.subplot(554)
# plt.tick_params(axis='both',labelbottom='off',labelleft='off')	
# plt.xlabel(r"$i-z$")

# plt.subplot(555)
# plt.tick_params(axis='both',labelleft='off')
# #plt.xticks([18,20,22,24],[18,20,22,24])
# plt.xlabel(r"$R_f(i)$")

plt.subplot(556)
plt.xlabel(r"$u-g$")
plt.ylabel(r"$R_f(i)$")
plt.xlim(0.5,2.0)
plt.plot(ug_colors,ratios,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(557)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.xlabel(r"$g-r$")
plt.xlim(0,1.2)
plt.plot(gr_colors,ratios,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(558)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.xlabel(r"$r-i$")
plt.xlim(0,0.8)
plt.plot(ri_colors,ratios,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(559)
plt.tick_params(axis='both',labelleft='off')
plt.xticks([-.2,-.1,0,.1,.2,.3],[-.2,-.1,0,.1,.2,.3])
plt.xlabel(r"$i-z$")
plt.xlim(-.2,0.5)
plt.plot(iz_colors,ratios,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(5,5,11)
plt.plot(badug,badiz,'m.',alpha=0.5,ms=1.5)
plt.plot(ug,iz, 'k.',alpha=0.5,ms=1.5)
plt.xlim(0.5,2.0)
plt.ylim(-.2,0.5)
plt.yticks([-.1,0,.1,.2,.3,.4],[-.1,0,.1,.2,.3,.4])
plt.xlabel(r"$u-g$")
plt.ylabel(r"$i-z$")
plt.plot(ug_colors,iz_colors,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(5,5,12)
plt.tick_params(axis='both',labelbottom='off',labelleft='off')
plt.plot(badgr,badiz,'m.',alpha=0.5,ms=1.5)
plt.plot(gr,iz,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,1.2)
plt.ylim(-.2,0.5)
plt.xlabel(r"$g-r$")
plt.plot(gr_colors,iz_colors,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(5,5,13)
plt.tick_params(axis='both',labelleft='off')
plt.plot(badri,badiz,'m.',alpha=0.5,ms=1.5)
plt.plot(ri,iz,'k.',alpha=0.5,ms=1.5)
plt.xlim(0,0.8)
plt.xticks([0.0,0.2,0.4,0.6,0.8],[0.0,0.2,0.4,0.6,0.8])
plt.ylim(-.2,0.5)
plt.xlabel(r"$r-i$")
plt.plot(ri_colors,iz_colors,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(5,5,16)
plt.plot(badug,badri,'m.',alpha=0.5,ms=1.5)
plt.plot(ug,ri,'k.',alpha=0.5,ms=1.5)
plt.xlim(0.5,2.0)
plt.ylim(0,0.8)
plt.yticks([0.0,0.2,0.4,0.6,0.8],[0.0,0.2,0.4,0.6,0.8])
plt.xlabel(r"$u-g$")
plt.ylabel(r"$r-i$")
plt.plot(ug_colors,ri_colors,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(5,5,17)
plt.tick_params(axis='both',labelleft='off')
plt.plot(badgr,badri,'m.',alpha=0.5,ms=1.5)
plt.plot(gr,ri,'k.',alpha=0.5,ms=1.5)		
plt.xlim(0,1.2)
plt.xticks([0.2,0.4,0.6,0.8,1.0],[0.2,0.4,0.6,0.8,1.0])
plt.ylim(0,0.8)
plt.xlabel(r"$g-r$")
plt.plot(gr_colors,ri_colors,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.subplot(5,5,21)
plt.plot(badug,badgr,'m.',alpha=0.5,ms=1.5)
plt.plot(ug,gr,'k.',alpha=0.5,ms=1.5)
plt.xlim(0.5,2.0)
plt.xlabel(r"$u-g$")
plt.yticks([0.2,0.4,0.6,0.8,1.0],[0.2,0.4,0.6,0.8,1.0])
plt.ylim(0,1.2)
plt.xticks([0.5,1.0,1.5,2.0],[0.5,1.0,1.5,2.0])
plt.ylabel(r"$g-r$")
plt.plot(ug_colors,gr_colors,'o',ms=2,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

plt.savefig('comparison_tractor.pdf')
os.system('cp comparison_tractor.pdf public_html')
