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
    print z[good].shape


#fnugriz
#0123456    
    def Mag1(y):
        return 22.5-2.5*np.log10(np.abs(y))     
    def SB(y):
        return 2.5*np.log10(2*np.pi*y)
    def concentration(x,y):
    	return x/y
    	
    
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

#NSA color distribution
fig1=plt.figure(1)
plt.plot(badgr,badri,'m.', alpha=0.5)
plt.plot(gr, ri,'k.', alpha=0.5)
plt.xlabel(r"$g-r$")
plt.ylabel(r"$r-i$")
plt.xlim(0,1.2)
plt.ylim(-.1,0.8)


#UNPICKLE STARTS HERE
#,3351,4192,4548,221,3368,4254,4594,3992,4501,4649,4374]
#4649 has bad results
ngcs=[4621,3351,4192,4548,221,3368,4254,4594,3992,4501,4374]
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

#get extinction from SFD
    x=get_SFD_dust(pos[0], pos[1],dustmap='ebv',interpolate=True)
    correction=[x*sloanu,x*sloang,x*sloanr,x*sloani,x*sloanz]
    corrected_mags=map(operator.sub,tot,correction)
    print corrected_mags
    tracgr=tot[1]-tot[2]
    tracri=tot[2]-tot[3]
    print tracgr
    print tracri
    gr_corrected=corrected_mags[1]-corrected_mags[2]
    ri_corrected=corrected_mags[2]-corrected_mags[3]
    print gr_corrected
    print ri_corrected

    color1=[tracgr, gr_corrected]
    color2=[tracri, ri_corrected]
    
    xyz=['red','yellow','blue','cyan','magenta','green','purple','orange']
    rando=choice(xyz)
    choosing=[t for t in xrange(len(xyz)) if rando == xyz[t]]
    for t in choosing:
        plt.plot(color1, color2,'*',linestyle='-', color=rando, ms=12, markeredgecolor=xyz[t] , markeredgewidth=1,markerfacecolor='none')

        
plt.savefig('colorplot_messier.pdf')
os.system('cp colorplot_messier.pdf public_html/')


fig2=plt.figure(2)
plt.subplot(121)
plt.title('tractor')
plt.plot(badgr,badri,'m.', alpha=0.5)
plt.plot(gr, ri,'k.', alpha=0.5)
plt.xlabel(r"$g-r$")
plt.ylabel(r"$r-i$")
plt.xlim(0,1.2)
plt.ylim(-.1,0.8)

for ngc in ngcs:
    print ngc
    CG=unpickle_from_file('ngc-%s.pickle'%(ngc)) 
    tot=CG.getBrightness()
    print tot

    tracgr=tot[1]-tot[2]
    tracri=tot[2]-tot[3]
    plt.plot(tracgr,tracri,'*', ms=12, markeredgecolor='cyan',markeredgewidth=1,markerfacecolor='none')


plt.subplot(122)
plt.title('tractor with extinction')
plt.plot(badgr,badri,'m.', alpha=0.5)
plt.plot(gr, ri,'k.', alpha=0.5)
plt.xlabel(r"$g-r$")
plt.ylabel(r"$r-i$")
plt.xlim(0,1.2)
plt.ylim(-.1,0.8)

for ngc in ngcs:
    print ngc
    CG=unpickle_from_file('ngc-%s.pickle'%(ngc)) 
    tot=CG.getBrightness()
    print tot
    pos=CG.getPosition()
    print pos
    dev=CG.brightnessDev
    print dev

#extinction values by filter for Sloan
    sloanu=5.155
    sloang=3.793
    sloanr=2.751
    sloani=2.086
    sloanz=1.479


#get extinction from SFD
    x=get_SFD_dust(pos[0], pos[1],dustmap='ebv',interpolate=True)
    correction=[x*sloanu,x*sloang,x*sloanr,x*sloani,x*sloanz]
    corrected_mags=map(operator.sub,tot,correction)
    print corrected_mags
    tracgr=tot[1]-tot[2]
    tracri=tot[2]-tot[3]
    gr_corrected=corrected_mags[1]-corrected_mags[2]
    ri_corrected=corrected_mags[2]-corrected_mags[3]
    plt.plot(gr_corrected,ri_corrected,'*', ms=12, markeredgecolor='orange',markeredgewidth=1,markerfacecolor='none')
plt.savefig('colorplot_messier2.pdf')
os.system('cp colorplot_messier2.pdf public_html/')

fig3=plt.figure(3)
plt.title('total, dev and exp mags')
plt.plot(badgr,badri,'m.', alpha=0.5,label='_nolegend_')
plt.plot(gr, ri,'k.', alpha=0.5,label='_nolegend_')
plt.xlabel(r"$g-r$")
plt.ylabel(r"$r-i$")
plt.xlim(0,1.2)
plt.ylim(-.1,0.8)

for ngc in ngcs:
    print ngc
    CG=unpickle_from_file('ngc-%s.pickle'%(ngc)) 
    tot=CG.getBrightness()
    print tot
    dev=CG.brightnessDev
    print dev
    exp = CG.brightnessExp
    print exp

    tracgr=tot[1]-tot[2]
    tracri=tot[2]-tot[3]
    devgr=dev[1]-dev[2]
    devri=dev[2]-dev[3]
    expgr=exp[1]-exp[2]
    expri=exp[2]-exp[3]
    color7=[expgr,tracgr,devgr]
    color8=[expri,tracri,devri]
    markers=itertools.cycle(['^-','*-','s-'])
    marker=markers.next

    # colors=['red','yellow','blue','cyan','magenta','green','purple','orange']
    # xyz=itertools.cycle(['red','yellow','blue','cyan','magenta','green','purple','orange'])
    # rando=xyz.next()
    xyz=['red','yellow','blue','cyan','magenta','green','purple','orange']
    rando=choice(xyz)
    choosing=[t for t in xrange(len(xyz)) if rando == xyz[t]]
    for t in choosing:
        for col7,col8 in zip(color7,color8):
            plt.plot(color7,color8,'-',color=rando)
            plt.plot(col7,col8,markers.next(), ms=11, markeredgecolor=xyz[t], markeredgewidth=1, markerfacecolor='none')


plt.savefig('colorplot_allmags.pdf')
os.system('cp colorplot_allmags.pdf public_html/')


fig4=plt.figure(4)
plt.title('total, dev, and exp mags distribution')
plt.plot(badgr,badri,'m.', alpha=0.5,label='_nolegend_')
plt.plot(gr, ri,'k.', alpha=0.5,label='_nolegend_')
plt.xlabel(r"$g-r$")
plt.ylabel(r"$r-i$")
plt.xlim(0,1.2)
plt.ylim(-.1,0.8)

for ngc in ngcs:
    print ngc
    CG=unpickle_from_file('ngc-%s.pickle'%(ngc)) 
    tot=CG.getBrightness()
    print tot
    dev=CG.brightnessDev
    print dev
    exp = CG.brightnessExp
    print exp

    tracgr=tot[1]-tot[2]
    tracri=tot[2]-tot[3]
    devgr=dev[1]-dev[2]
    devri=dev[2]-dev[3]
    expgr=exp[1]-exp[2]
    expri=exp[2]-exp[3]
    color3=[tracgr,devgr]
    color4=[tracri,devri]
    color5=[expgr,tracgr]
    color6=[expri,tracri]
   
    plt.plot(tracgr,tracri,'*', linestyle='-', color='c',ms=12, markeredgecolor='c',markeredgewidth=1,markerfacecolor='none')     
    plt.plot(devgr,devri,'s', linestyle='-', color='y',ms=12, markeredgecolor='y',markeredgewidth=1,markerfacecolor='none')     
    plt.plot(expgr,expri,'^',linestyle='-', color='r', ms=12, markeredgecolor='r',markeredgewidth=1,markerfacecolor='none')     
label1='bad colors'
label2='good colors'
label3='total mags'
label4='dev mags'
label5='exp mags'   
#plt.legend((label3,label4,label5),loc='lower right')

plt.savefig('colorplot_allmags2.pdf')
os.system('cp colorplot_allmags2.pdf public_html/')
