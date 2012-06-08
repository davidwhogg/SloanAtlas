import matplotlib
matplotlib.use('Agg')
import numpy as np
import pylab as plt
import pyfits as pyf
import os
from yanny import *


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

def allImages(title,nsaid2,samplename,t):
	page = r'''
	\frame{
	\textbf{%s}
    \includegraphics[scale=0.20]{%s.jpg}
    \includegraphics[scale=0.25]{%s_plot3.pdf}\\
    NSAID: %s
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
	if int(nsaid2) in nsaid:
		for i in range(len(nsaid)):
			if nsaid[i]==int(nsaid2):
				temp+= page % (title,nsaid2,samplename,e[good][t],a[good][t], b[good][t],z[good][t],(p90[good][t])/60,f[good][t],ug[t], gr[t], ri[t], iz[t],r[t], comment[i],nsauser[i],time[i])
	else:
		temp=page % (title,nsaid2,samplename,e[good][t],a[good][t], b[good][t],z[good][t],(p90[good][t])/60,f[good][t],ug[t], gr[t], ri[t], iz[t],r[t],'none','none','none')			
	return temp
    

	
tex+=allImages('exemplar: color sample 0, i-sb sample 0', '88297','exemplar01',757)
tex+=allImages('exemplar: color sample 0, i-sb sample 1', '158651','exemplar02',1882)
tex+=allImages('exemplar: color sample 0, i-sb sample 2', '74038','exemplar03', 643)
tex+=allImages('exemplar: color sample 0, i-sb sample 3', '143102', 'exemplar04',1568)
tex+=allImages('exemplar: color sample 1, i-sb sample 0', '88298', 'exemplar05',758)
tex+=allImages('exemplar: color sample 1, i-sb sample 1', '158585', 'exemplar06',1879)
tex+=allImages('exemplar: color sample 1, i-sb sample 2', '31572' , 'exemplar07',256)
tex+=allImages('exemplar: color sample 1, i-sb sample 3', '44000', 'exemplar08',352)
tex+=allImages('exemplar: color sample 2, i-sb sample 0', '166141', 'exemplar09',2035)
tex+=allImages('exemplar: color sample 2, i-sb sample 1', '126043', 'exemplar10',1018)
tex+=allImages('exemplar: color sample 2, i-sb sample 2', '54244', 'exemplar11',445)
tex+=allImages('exemplar: color sample 2, i-sb sample 3', '5029', 'exemplar12',40)
tex+=allImages('exemplar: color smaple 3, i-sb sample 0', '83634', 'exemplar13',722)
tex+=allImages('exemplar: color sample 3, i-sb sample 1', '162413', 'exemplar14',1982)
tex+=allImages('exemplar: color sample 3, i-sb sample 2', '155176', 'exemplar15',1832)
tex+=allImages('exemplar: color sample 3, i-sb sample 3', '139151', 'exemplar16',1335)
tex+=allImages('smallest: color sample 0, i-sb sample 0', '141654', 'smallest01',1475)
tex+=allImages('smallest: color sample 0, i-sb sample 1', '162575', 'smallest02',1986)
tex+=allImages('smallest: color sample 0, i-sb sample 2', '165451', 'smallest03',2023)
tex+=allImages('smallest: color sample 0, i-sb sample 3', '44545', 'smallest04',366)
tex+=allImages('smallest: color sample 1, i-sb sample 0', '137237', 'smallest05',1297)
tex+=allImages('smallest: color sample 1, i-sb sample 1', '129827', 'smallest06',1114)
tex+=allImages('smallest: color sample 1, i-sb sample 2', '8756', 'smallest07',76)
tex+=allImages('smallest: color sample 1, i-sb sample 3', '115565', 'smallest08',957)
tex+=allImages('smallest: color sample 2, i-sb sample 0', '93093','smallest09',807)
tex+=allImages('smallest: color sample 2, i-sb sample 1', '76778', 'smallest10',662)
tex+=allImages('smallest: color sample 2, i-sb sample 2', '133790','smallest11',1221)
tex+=allImages('smallest: color sample 2, i-sb sample 3', '66672', 'smallest12',554)
tex+=allImages('smallest: color sample 3, i-sb sample 0', '141473', 'smallest13',1451)
tex+=allImages('smallest: color sample 3, i-sb sample 1', '91658', 'smallest14',791)
tex+=allImages('smallest: color sample 3, i-sb sample 2', '136051', 'smallest15',1273)
tex+=allImages('smallest: color sample 3, i-sb sample  3', '98900', 'smallest16',844)
tex+=allImages('random: color sample 0, i-sb sample 0', '142962', 'random01',1555)
tex+=allImages('random: color sample 0, i-sb sample 1', '138272', 'random02',1317)
tex+=allImages('random: color sample 0, i-sb sample 2', '69210', 'random03',604)
tex+=allImages('random: color sample 0, i-sb sample 3', '28067', 'random04',227)
tex+=allImages('random: color sample 1, i-sb sample 0', '154089', 'random05',1816)
tex+=allImages('random: color sample 1, i-sb sample 1', '142446', 'random06',1525)
tex+=allImages('random: color sample 1, i-sb sample 2', '146349', 'random07',1681)
tex+=allImages('random: color sample 1, i-sb sample 3', '140045', 'random08',1358)
tex+=allImages('random: color sample 2, i-sb sample 0', '149192','random09',1735)
tex+=allImages('random: color sample 2, i-sb sample 1', '145871', 'random10',1666)
tex+=allImages('random: color sample 2, i-sb sample 2', '157310','random11',1862)
tex+=allImages('random: color sample 2, i-sb sample 3', '96631', 'random12',828)
tex+=allImages('random: color sample 3, i-sb sample 0', '162027', 'random13',1963)
tex+=allImages('random: color sample 3, i-sb sample 1', '140952', 'random14',1400)
tex+=allImages('random: color sample 3, i-sb sample 2', '140377', 'random15',1374)
tex+=allImages('random: color sample 3, i-sb sample  3', '155051', 'random16',1827)


tex += r'\end{document}' + '\n'
fn = 'flip-' + 'prospectus-comments' + '.tex' 
print 'Writing', fn
open(fn, 'wb').write(tex)
os.system("pdflatex '%s'" % fn)
