#created prospectus plots for galaxies in hubble
import matplotlib
matplotlib.use('Agg')
import numpy as np
import pylab as plt
import pyfits as pyf
import os
from yanny import *
import Image

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    a=data.field('RA')
    b=data.field('DEC')
    y=data.field('SERSICFLUX')
    z = data.field('SERSIC_TH50')
    w=data.field('IAUNAME')
    e=data.field('NSAID')
    f=data.field('DFLAGS')
    p50=data.field('PETROTH50')
    p90=data.field('PETROTH90')
    good=np.array([True for x in data.field('RA')])
    indx1=np.where(y[:,3] <= 0)
    good[indx1]=False
    indx2=np.where(y[:,1] <= 0)
    good[indx2]=False
    indx3=np.where(z >= 158)
    good[indx3]=False
    
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
def resize(x):
	imagefile="%s.jpg" %(x)
	im1=Image.open(imagefile)
	width=640
	height=640
	im2=im1.resize((width,height),Image.ANTIALIAS)
	#im2.show()
	im3=im2.save("%s_.jpeg" %(x)) 
	return im2
	
#magnitudes
u=Mag1(y[:,0][good])
g=Mag1(y[:,1][good]) 
r=Mag1(y[:,2][good])
i=Mag1(y[:,3][good])
zmag=Mag1(y[:,4][good])
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

#starting tex document  
tex=r''' 
\documentclass[8pt]{beamer}
\addtolength{\topmargin}{2pt}
\usepackage{helvet}
\usepackage{graphicx}
\begin{document}
'''

def allImages(title,hubble,nsaid2,samplename,t):
	page = r'''
	\frame{
	\textbf{%s}\hspace{180pt} \textit{title: %s} \\
    \includegraphics[scale=0.20]{%s_.jpeg}
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
				temp+= page % (title,hubble,nsaid2,samplename,im1.size, e[good][t],a[good][t], b[good][t],z[good][t],(p90[good][t])/60,f[good][t],ug[t], gr[t], ri[t], iz[t],r[t], comment[i],nsauser[i],time[i])
	else:
		temp=page % (title,hubble,nsaid2,samplename,im1.size,e[good][t],a[good][t], b[good][t],z[good][t],(p90[good][t])/60,f[good][t],ug[t], gr[t], ri[t], iz[t],r[t],'none','none','none')			
	return temp
	
tex+=allImages('NGC 751 (w/ NGC 750)','E0', '154728','hubble01',1822)
tex+=allImages('NGC 4697','E5', '142365','hubble02',1515)
tex+=allImages('NGC 524','S0$_2$', '129461','hubble03',1105)
tex+=allImages('NGC 4274','Sa', '141155','hubble04',1420)
tex+=allImages('NGC 4569','Sb', '141717','hubble05',1484)
tex+=allImages('NGC 3810','Sc', '160362','hubble06',1914)
tex+=allImages('NGC 2859','SB0$_2$', '172734','hubble07',2118)
tex+=allImages('NGC 3185','SBa(s)', '108448','hubble08',911)
tex+=allImages('NGC 5383','SBb(s)', '144151','hubble09',1602)
tex+=allImages('NGC 7741','SBc(s)', '152489','hubble10',1796)
tex+=allImages('NGC 520','Irr II', '154180','hubble11',1818)

tex += r'\end{document}' + '\n'
fn = 'flip-' + 'hubble' + '.tex' 
print 'Writing', fn
open(fn, 'wb').write(tex)
os.system("pdflatex '%s'" % fn)
