#creates plots that compare the Messier output from tractor to the extinction corrected  NS Atlas galaxies and then makes them into a beamer tex file
from astrometry.util.file import *
from astrometry.util.starutil_numpy import *
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pylab as plt
import pyfits as pyf
from astropysics.obstools import *
import operator
import math
import os
import sys
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
    extinction=data.field('EXTINCTION')
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
u=map(operator.sub,Mag1(y[:,2][good]),extinction[:,2][good])
g=map(operator.sub,Mag1(y[:,3][good]),extinction[:,3][good])
r=map(operator.sub,Mag1(y[:,4][good]),extinction[:,4][good])
i=map(operator.sub,Mag1(y[:,5][good]),extinction[:,5][good])
zmag=map(operator.sub,Mag1(y[:,6][good]),extinction[:,6][good])
badu=map(operator.sub,Mag1(y[:,2][good==False]),extinction[:,2][good==False])
badg=map(operator.sub,Mag1(y[:,3][good==False]),extinction[:,3][good==False])
badr=map(operator.sub,Mag1(y[:,4][good==False]),extinction[:,4][good==False])
badi=map(operator.sub,Mag1(y[:,5][good==False]),extinction[:,5][good==False])
badz=map(operator.sub,Mag1(y[:,6][good==False]),extinction[:,6][good==False])
   
#colors
gi=map(operator.sub,g,i)
ug=map(operator.sub,u,g)
gr=map(operator.sub,g,r)
ri=map(operator.sub,r,i) 
iz=map(operator.sub,i,zmag)
badgi=map(operator.sub,badg,badi)
badug=map(operator.sub,badu,badg)
badgr=map(operator.sub,badg,badr)
badri=map(operator.sub,badr,badi)
badiz=map(operator.sub,badi,badz) 

#extinction values by filter for Sloan
sloanu=5.155
sloang=3.793
sloanr=2.751
sloani=2.086
sloanz=1.479

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
ngcs=[221,628,3034,3351,3368,3379,3623,3556,3627,3992,4192,4254,4321,4374,4382,4406,4472,4486,4501,4548,4552,4569,4579,4594,4621,4736,4826,5055,5194]
for ngc in ngcs:
    print ngc
    CG=unpickle_from_file('ngc-%s.pickle'%(ngc)) 
    tot=CG.getBrightness()
    print tot
    pos=CG.getPosition()
    print pos

#get extinction from SFD
    galactic=radectolb(pos[0],pos[1])
    print galactic
    x=get_SFD_dust(galactic[0], galactic[1],dustmap='ebv',interpolate=True)
    correction=[x*sloanu,x*sloang,x*sloanr,x*sloani,x*sloanz]
    corrected_mags=map(operator.sub,tot,correction)
    print corrected_mags
    tracgr=tot[1]-tot[2]
    tracri=tot[2]-tot[3]
#    print tracgr
#    print tracri
    gr_corrected=corrected_mags[1]-corrected_mags[2]
    ri_corrected=corrected_mags[2]-corrected_mags[3]
#    print gr_corrected
#    print ri_corrected

    color1=[tracgr, gr_corrected]
    color2=[tracri, ri_corrected]
    
    xyz=['red','yellow','blue','cyan','magenta','green','purple','orange']
    rando=choice(xyz)
    choosing=[t for t in xrange(len(xyz)) if rando == xyz[t]]
    for t in choosing:
        plt.plot(color1, color2,'*',linestyle='-', color=rando, ms=12, markeredgecolor=xyz[t] , markeredgewidth=1,markerfacecolor='none')
        
plt.savefig('test_messier1.pdf')
os.system('cp test_messier1.pdf public_html/messiercomparisons/')


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

#get extinction from SFD
    galactic=radectolb(pos[0],pos[1])
    print galactic
    x=get_SFD_dust(galactic[0], galactic[1],dustmap='ebv',interpolate=True)
    correction=[x*sloanu,x*sloang,x*sloanr,x*sloani,x*sloanz]
    corrected_mags=map(operator.sub,tot,correction)
    print corrected_mags
    gr_corrected=corrected_mags[1]-corrected_mags[2]
    ri_corrected=corrected_mags[2]-corrected_mags[3]
    plt.plot(gr_corrected,ri_corrected,'*', ms=10, markeredgecolor='orange',markeredgewidth=1,markerfacecolor='none')

plt.savefig('test_messier2.pdf')
os.system('cp test_messier2.pdf public_html/messiercomparisons/')

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

label1='bad colors'
label2='good colors'
label3='all mags'
label4='exp,total,dev'
#plt.legend(label4, loc='lower right')
plt.savefig('test_messier3.pdf')
os.system('cp test_messier3.pdf public_html/messiercomparisons/')


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
 #   print tot
    dev=CG.brightnessDev
 #   print dev
    exp = CG.brightnessExp
 #   print exp

    tracgr=tot[1]-tot[2]
    tracri=tot[2]-tot[3]
    devgr=dev[1]-dev[2]
    devri=dev[2]-dev[3]
    expgr=exp[1]-exp[2]
    expri=exp[2]-exp[3]
   
    plt.plot(tracgr,tracri,'*', linestyle='-', color='c',ms=10, markeredgecolor='c',markeredgewidth=1,markerfacecolor='none')     
    plt.plot(devgr,devri,'s', linestyle='-', color='y',ms=10, markeredgecolor='y',markeredgewidth=1,markerfacecolor='none')     
    plt.plot(expgr,expri,'^',linestyle='-', color='r', ms=10, markeredgecolor='r',markeredgewidth=1,markerfacecolor='none')     
label1='bad colors'
label2='good colors'
label3='total mags'
label4='dev mags'
label5='exp mags'   
plt.legend((label3,label4,label5),loc='lower right')

plt.savefig('test_messier4.pdf')
os.system('cp test_messier4.pdf public_html/messiercomparisons/')


fig5=plt.figure(5)
plt.title('total, dev, and exp mags distribution with extinction')
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
#    print tot
    dev=CG.brightnessDev
#    print dev
    exp = CG.brightnessExp
#    print exp
    
#get extinction from SFD
    galactic=radectolb(pos[0],pos[1])
    print galactic
    x=get_SFD_dust(galactic[0], galactic[1],dustmap='ebv',interpolate=True)
    correction=[x*sloanu,x*sloang,x*sloanr,x*sloani,x*sloanz]
    corrected_mags=map(operator.sub,tot,correction)
    corrected_dev=map(operator.sub,dev,correction)
    corrected_exp=map(operator.sub,exp,correction)
#corrected total mags
    gr_corrected=corrected_mags[1]-corrected_mags[2]
    ri_corrected=corrected_mags[2]-corrected_mags[3]
#corrected dev mags
    gr_dev=corrected_dev[1]-corrected_dev[2]
    ri_dev=corrected_dev[2]-corrected_dev[3]
#corrected exp mags
    gr_exp=corrected_exp[1]-corrected_exp[2]
    ri_exp=corrected_exp[2]-corrected_exp[3]
   
    plt.plot(gr_corrected,ri_corrected,'*', linestyle='-', color='c',ms=10, markeredgecolor='c',markeredgewidth=1,markerfacecolor='none')     
    plt.plot(gr_dev,ri_dev,'s', linestyle='-', color='y',ms=10, markeredgecolor='y',markeredgewidth=1,markerfacecolor='none')     
    plt.plot(gr_exp,ri_exp,'^',linestyle='-', color='r', ms=10, markeredgecolor='r',markeredgewidth=1,markerfacecolor='none')     

label1='bad colors'
label2='good colors'
label3='total mags'
label4='dev mags'
label5='exp mags'   
plt.legend((label3,label4,label5),loc='lower right')
plt.savefig('test_messier5.pdf')
os.system('cp test_messier5.pdf public_html/messiercomparisons/')

tex=r'''
\documentclass[8pt]{beamer}
\usepackage{helvet}
\usepackage{graphicx}
\begin{document}
\frame{
\includegraphics[scale=.5]{test_messier1.pdf}
\newline \tiny Figure 1. The color distribution of a selected set of Nasa-Sloan Atlas galaxies is provided in the background of this plot. 'Good' data has been identified with black points, while 'bad' data is given in magenta. The criteria for bad data include galaxies with negative fluxes in the \textit{i} and \textit{g} bands as well as any galaxy with a half-light radius of 158 arcsec or greater.This distribution has also been corrected for extinction. Each pair of connected stars represents the original and SFD dust map corrected colors for Messier galaxies that have been fitted with \textit{Tractor}.}
\frame{
\includegraphics[scale=.5]{test_messier2.pdf}
\newline \tiny Figure 2. The background color distribution is the same set of Nasa-Sloan Atlas galaxies with identical parameters as those described in Figure 1. In the left panel, each star represents the colors of a Messier galaxy fitted by \textit{Tractor}. The colors here are calculated from the combined Exp and deV magnitudes. In the right panel, the \textit{Tractor} colors for each galaxy are plotted again, but the magnitudes have been corrected for extinction with the SFD Dust maps before colors were calculated.}
\frame{
\includegraphics[scale=.5]{test_messier3.pdf}
\newline \tiny Figure 3. In addition to the Nasa-Sloan color distribution, this plot provides three different colors for each Messier galaxy fitted by \textit{Tractor}. The triangles show the color resulting from the non-extinction corrected color calculated from the Exp magnitudes. The square gives the colors resulting from the non-extinction corrected deV magnitudes. The star gives the non-extinction corrected color resulting from the combined magnitudes. }
\frame{
\includegraphics[scale=.5]{test_messier4.pdf}
\newline \tiny Figure 4. The \textit{Tractor} output and symbols remain the same as described above in Figure 3, but this plot shows the distribution of all non-extinction corrected colors of the Messier galaxies.}
\frame{
\includegraphics[scale=.5]{test_messier5.pdf}
\newline \tiny Figure 5. This contains the same NASA-Sloan data as mentioned above. However, the stars that represent each Messier galaxy are extinction corrected with the SFD dust maps in the colors given by each of the three magnitudes output by \textit{Tractor}.} 
\end{document}'''



fn='messier'+'.tex'
print 'Writing' ,fn
open(fn,'wb').write(tex)
os.system("pdflatex '%s'" %(fn))
os.system('cp messier.pdf public_html/messiercomparisons/')

