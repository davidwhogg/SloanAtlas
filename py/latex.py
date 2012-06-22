#created prospectus plots (48) with tex formatting
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pylab as plt
import pyfits as pyf
import os
import sys    
import Image
import urllib
from yanny import *
from decimal import *
from astrometry.util.starutil_numpy import *
from astrometry.libkd import spherematch as sm

if __name__ == '__main__':
    data = pyf.open("nsa-short.fits.gz")[1].data
    a=data.field('RA')
    b=data.field('DEC')
    y=data.field('SERSICFLUX')
    radius = data.field('SERSIC_TH50')
    w=data.field('IAUNAME')
    e=data.field('NSAID')
    f=data.field('DFLAGS')
    z = data.field('SERSIC_TH50')
    n=data.field('SERSIC_N')
    p50=data.field('PETROTH50')
    p90=data.field('PETROTH90')
    good=np.array([True for x in data.field('RA')])
    indx1=np.where(y[:,5] <= 0)
    good[indx1]=False
    indx2=np.where(y[:,3] <= 0)
    good[indx2]=False
    indx3=np.where(radius >= 158)
    good[indx3]=False
  
    data2= pyf.open('GalaxyZoo1_DR_table2.fits')[1].data
    RA=data2.field('RA')
    DEC=data2.field('DEC')
    type1=data2.field('P_EL')
    type2=data2.field('P_CW')
    type3=data2.field('P_ACW')
    type4=data2.field('P_EDGE')
    type5=data2.field('P_DK')
    type6=data2.field('P_MG')
    type7=data2.field('P_CS')
      
nsa = read_yanny('comments.par')
comments = nsa['COMMENT']      
comment = comments['comment']
nsauser = comments['nsauser']
nsaid   = comments['nsaid']
time    = comments['time'] 
   
def Mag1(y):
    return 22.5-2.5*np.log10(np.abs(y))     
def SB(y):
    return 2.5*np.log10(2*np.pi*y) 
def concentration(x,y):
    return x/y
#find and resize image
def getimage(x):
    nocom = [t for t in xrange(len(e[good])) if e[good][t]==x]
    for t in nocom:       
        if b[good][t] > 0: 
       		url='http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/p%02d/%s/%s.jpg' %(w[good][t][1:3],((int(w[good][t][11:13]))/2)*2,w[good][t],w[good][t])
        else: 
                url='http://sdss.physics.nyu.edu/mblanton/v0/detect/v0_1/%sh/m%02d/%s/%s.jpg' %(w[good][t][1:3],((int(w[good][t][11:13]))/2)*2,w[good][t],w[good][t])

    urllib.urlretrieve(url, '%s.jpg' %(x))
    print url

def resize(x):
    imagefile="%s.jpg" %(x)
    im1=Image.open(imagefile)
    width=640
    height=640
    im2=im1.resize((width,height),Image.ANTIALIAS)
    im3=im2.save("%s_.jpeg" %(x)) 
    return im2

#use gzoo to find equivalent galaxies for classification
def find(t):
    for i in xrange(len(RA)):
        ra1=hmsstring2ra(RA[i]) + arcmin2deg(1)
        ra2=hmsstring2ra(RA[i]) - arcmin2deg(1)
        dec1=dmsstring2dec(DEC[i])+arcmin2deg(1)
        dec2=dmsstring2dec(DEC[i])-arcmin2deg(1)        
        if ra2 < a[good][t] < ra1 and  dec2 < b[good][t] < dec1:
            x=[type1[i],type2[i],type3[i], type4[i], type5[i], type6[i], type7[i]]  
            print x
            classes=["elliptical","clockwise","anti-clockwise","edge-on","dont know" ,"merger", "combined spiral"]
            y=max(x)
            print y
            for i in xrange(len(x)):
                if x[i]==max(x): 
                    return y, classes[i]
    return None

	
#magnitudes
u=Mag1(y[:,2][good])
g=Mag1(y[:,3][good]) 
r=Mag1(y[:,4][good])
i=Mag1(y[:,5][good])
zmag=Mag1(y[:,6][good])
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
iz=i-zmag 
badgi=badg-badi
badug=badu-badg
badgr=badg-badr
badri=badr-badi
badiz=badi-badz 

####creating the triangle comparison plot
#i-magnitudes    
i1=Mag1(y[:,5][good])
i2=Mag1(y[:,5][indx1])
i3=Mag1(y[:,5][indx3])
    
#radii
radii=radius[good]
badradii=radius[good==False]
    
#concentrations
c=concentration(p90[good],p50[good])
badc=concentration(p90[good==False],p50[good==False])    
	
#i-surface brightnesses       
sb=i+SB(z[good])
badsb=badi+SB(badradii)

#sersic index
sersic=n[good]
badsersic=n[good==False]

def plot(nsaid2):
    get_t=[t for t in xrange(len(a[good])) if nsaid2==e[good][t]]
    for t in get_t:
        print t
	plt.figure(figsize=(8,8))
	plt.subplots_adjust(wspace=0,hspace=0)
	matplotlib.rcParams['font.size'] = 9

	plt.subplot(551)
	plt.plot(badug,badsersic,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0.5,2.0)
	plt.ylim(0.5,6.1)
	plt.xlabel(r"$u-g$")
	plt.ylabel('n')
	plt.plot(ug[t],sersic[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(552)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badgr,badsersic,'m.',alpha=0.5,ms=1.5)
	plt.plot(gr,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,1.2)
	plt.ylim(0.5,6.1)
	plt.xlabel(r"$g-r$")
	plt.plot(gr[t],sersic[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(553)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badri,badsersic,'m.',alpha=0.5,ms=1.5)
	plt.plot(ri,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,0.8)
	plt.ylim(0.5,6.1)
	plt.xlabel(r"$r-i$")
	plt.plot(ri[t],sersic[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(554)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badiz,badsersic,'k.',alpha=0.5,ms=1.5)
	plt.plot(iz,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(-.2,0.5)
	plt.ylim(0.5,6.1)
	plt.xlabel(r"$i-z$")
	plt.plot(iz[t],sersic[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(555)
	plt.tick_params(axis='both',labelleft='off')
	plt.plot(badsb,badsersic,'m.',alpha=0.5,ms=1.5)
	plt.plot(sb,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(17,24)
	plt.xticks([18,20,22,24],[18,20,22,24])
	plt.ylim(0.5,6.1)
	plt.xlabel(r"$\mu_i$")
	plt.plot(sb[t],sersic[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(556)
	plt.plot(badug,badsb,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,sb,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0.5,2.0)
	plt.ylim(17,24)
	plt.yticks([18,20,22,24],[18,20,22,24])
	plt.xlabel(r"$u-g$")
	plt.ylabel(r"$\mu_i$")
	plt.plot(ug[t],sb[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(557)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badgr,badsb,'m.',alpha=0.5,ms=1.5)
	plt.plot(gr,sb,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,1.2)
	plt.ylim(17,24)
	plt.xlabel(r"$g-r$")
	plt.plot(gr[t],sb[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(558)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badri,badsb,'m.',alpha=0.5,ms=1.5)
	plt.plot(ri,sb,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,0.8)
	plt.ylim(17,24)
	plt.xlabel(r"$r-i$")
	plt.plot(ri[t],sb[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(559)
	plt.tick_params(axis='both',labelleft='off')
	plt.plot(badiz,badsb,'k.',alpha=0.5,ms=1.5)
	plt.plot(iz,sb,'k.',alpha=0.5,ms=1.5)
	plt.xlim(-.2,0.5)
	plt.xticks([-.1,0,.1,.2,.3,.4],[-.1,0,.1,.2,.3,.4])
	plt.ylim(17,24)
	plt.xlabel(r"$i-z$")
	plt.plot(iz[t],sb[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,11)
	plt.plot(badug,badiz,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,iz,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0.5,2.0)
	plt.ylim(-.2,0.5)
	plt.yticks([-.1,0,.1,.2,.3,.4],[-.1,0,.1,.2,.3,.4])
	plt.xlabel(r"$u-g$")
	plt.ylabel(r"$i-z$")
	plt.plot(ug[t],iz[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,12)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badgr,badiz,'m.',alpha=0.5,ms=1.5)
	plt.plot(gr,iz,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,1.2)
	plt.ylim(-.2,0.5)
	plt.xlabel(r"$g-r$")
	plt.plot(gr[t],iz[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,13)
	plt.tick_params(axis='both',labelleft='off')
	plt.plot(badri,badiz,'m.',alpha=0.5,ms=1.5)
	plt.plot(ri,iz,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,0.8)
	plt.xticks([0.0,0.2,0.4,0.6,0.8],[0.0,0.2,0.4,0.6,0.8])
	plt.ylim(-.2,0.5)
	plt.xlabel(r"$r-i$")
	plt.plot(ri[t],iz[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,16)
	plt.plot(badug,badri,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,ri,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0.5,2.0)
	plt.ylim(0,0.8)
	plt.yticks([0.0,0.2,0.4,0.6,0.8],[0.0,0.2,0.4,0.6,0.8])
	plt.xlabel(r"$u-g$")
	plt.ylabel(r"$r-i$")
	plt.plot(ug[t],ri[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,17)
	plt.tick_params(axis='both',labelleft='off')
	plt.plot(badgr,badri,'m.',alpha=0.5,ms=1.5)
	plt.plot(gr,ri,'k.',alpha=0.5,ms=1.5)		
	plt.xlim(0,1.2)
	plt.xticks([0.2,0.4,0.6,0.8,1.0],[0.2,0.4,0.6,0.8,1.0])
	plt.ylim(0,0.8)
	plt.xlabel(r"$g-r$")
	plt.plot(gr[t],ri[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,21)
	plt.plot(badug,badgr,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,gr,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0.5,2.0)
	plt.xlabel(r"$u-g$")
	plt.yticks([0.2,0.4,0.6,0.8,1.0],[0.2,0.4,0.6,0.8,1.0])
	plt.ylim(0,1.2)
	plt.xticks([0.5,1.0,1.5,2.0],[0.5,1.0,1.5,2.0])
	plt.ylabel(r"$g-r$")
	plt.plot(ug[t],gr[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

        plt.suptitle('%s' % e[good][t]) 
        plt.savefig('%s_plot.pdf' % nsaid2) 
        x=plt.show()
    return x

#starting tex document  
tex=r''' 
\documentclass[8pt]{beamer}
\addtolength{\topmargin}{2pt}
\usepackage{helvet}
\usepackage{graphicx}
\begin{document}
'''

def allImages(title,nsaid2,t):
    page = r'''
    \frame{	
    \textbf{%s}\hspace{100pt} \textit{title:%s} \\
    \includegraphics[scale=0.19]{%s_.jpeg}
    \includegraphics[scale=0.25]{%s_plot.pdf}\\
    {\tiny %s image}
    \newline NSAID: %s					
    \newline RA: %s
    \newline Dec: %s	
    \newline Radius (arcsec): %s
    \newline Petrosian90 (arcmin): %s
    \newline Dflags: %s
    \newline colors: %s , %s , %s, %s 
    \newline r magnitude: %s
    \newline comment: %s
    \newline nsauser: %s
    \newline time: %s}'''
    temp=''

    
    resize(nsaid2)
    
    im1=Image.open("%s.jpg" %(nsaid2))
    
    if int(nsaid2) in nsaid:
        for i in range(len(nsaid)):
            if nsaid[i]==int(nsaid2):
                temp+= page % (title,find(t),nsaid2,nsaid2,im1.size, e[good][t],a[good][t], b[good][t],radius[good][t],(p90[good][t])/60,f[good][t],ug[t], gr[t], ri[t], iz[t],r[t], comment[i],nsauser[i],time[i])
    else:
        temp=page % (title,find(t),nsaid2,nsaid2,im1.size,e[good][t],a[good][t], b[good][t],radius[good][t],(p90[good][t])/60,f[good][t],ug[t], gr[t],ri[t], iz[t],r[t],'none','none','none')
 
    return temp
###end of frame info

getimage(1578)
plot(1578)    	
tex+=allImages('random1', '1578',10)

getimage(2910)
plot(2910)    	
tex+=allImages('random2', '2910',20)

getimage(5282)
plot(5282)    	
tex+=allImages('random3', '5282',50)

getimage(9549)
plot(9549)    	
tex+=allImages('random4', '9549',100)

getimage(14792)
plot(14792)    	
tex+=allImages('random5', '14792',150)

getimage(21448)
plot(21448)    	
tex+=allImages('random6', '21448',200)

getimage(26781)
plot(26781)    	
tex+=allImages('random7', '26781',250)

getimage(31572)
plot(31572)    	
tex+=allImages('random8', '31572',300)

getimage(37123)
plot(37123)    	
tex+=allImages('random9', '37123',350)

getimage(42502)
plot(42502)    	
tex+=allImages('random10', '42502',400)

getimage(45162)
plot(45162)    	
tex+=allImages('random11', '45162',450)

getimage(50644)
plot(50644)    	
tex+=allImages('random12', '50644',500)

getimage(56347)
plot(56347)    	
tex+=allImages('random13', '56347',550)

getimage(61396)
plot(61396)    	
tex+=allImages('random14', '61396',600)

getimage(65970)
plot(65970)    	
tex+=allImages('random15', '65970',650)

getimage(67938)
plot(67938)    	
tex+=allImages('random16', '67938',700)

getimage(72627)
plot(72627)    	
tex+=allImages('random17', '72627',750)

getimage(78212)
plot(78212)    	
tex+=allImages('random18', '78212',800)

getimage(83532)
plot(83532)    	
tex+=allImages('random19', '83532',850)

getimage(89205)
plot(89205)    	
tex+=allImages('random20', '89205',900)



tex += r'\end{document}' + '\n'
fn = 'flip-' + 'prospectus-titles' + '.tex' 
print 'Writing', fn
open(fn, 'wb').write(tex)
os.system("pdflatex '%s'" % fn)



#ab=sm.match_radec(a[50],b[50],map(hmsstring2ra,d),map(dmsstring2dec,e),1/60.)
#print ab
    


