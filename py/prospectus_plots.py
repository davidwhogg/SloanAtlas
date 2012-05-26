#prospectus for any general galaxy
#finds the good index of specified nsaid (given by t below..replaced 141119 and 1416)
#edits the i-sb vs. color plot to place a yellow star where the galaxy is located (need the coordinates first)
#edits the radius vs. concentration plot to place a cyan star where the galaxy is located (need coords)
#finds text of important properties
#compiles all into one plot (2 plots, galaxy pic, info)

import matplotlib
import numpy as np
import pylab as plt
import pyfits as pyf
import os
import Image

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    a=data.field('RA')
    b=data.field('DEC')
    e=data.field('NSAID')
    f=data.field('DFLAGS')
    w=data.field('IAUNAME')
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

    def Mag1(y):
        return 22.5-2.5*np.log10(np.abs(y))     
    def SB(y):
        return 2.5*np.log10(2*np.pi*y)
    def concentration(x,y):
    	return x/y

#getting info

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
sb=i+SB(z[good]) #i-sb from good values
badsb=badi+SB(badradii)
    	
print gi[1416] #for coords
print sb[1416]
print c[1416]

fig1=plt.figure(1)
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
plt.plot(16.1302,3.13061,'*',ms=18,markeredgecolor='yellow',markeredgewidth=1.1,markerfacecolor='none')
plt.savefig('ngc4258.png')

#radius vs. radius concentration
fig2=plt.figure(2)
plt.plot(badradii,badc, 'm.',alpha=0.5, label='bad')
plt.plot(radii,c,'k.',alpha=0.5,label='good')
plt.xlabel('Half-Light Radius (arcsec)')
plt.ylabel('Concentration (p90/p50)')
plt.xlim(29,161)
plt.ylim(0,4) 
plt.plot(98.8767,2.17244,'*',  ms=16,markeredgecolor='blue',markeredgewidth=1.1,markerfacecolor='none')
plt.savefig('ngc4258_c.png')  

#creating compiled plot

fig3=plt.figure(3,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1)
#plot with star
plt.subplot(222)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('ngc4258.png')
plt.imshow(im,origin='lower')

plt.subplot(224)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('ngc4258_c.png')
plt.imshow(im,origin='lower')

#galaxy
plt.subplot(221)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('141119.jpg')
plt.imshow(im,origin='lower')

#text
find=[t for t in xrange(len(e[good])) if e[good][t]==141119]
for t in find:
	print t	
	print 'NSAID:',e[good][t]
	print 'IAU Name:', w[good][t]
	print 'RA:', a[good][t]
	print 'Dec:', b[good][t]
	print 'Radius:',z[good][t]
	print 'Dflags:',f[good][t]
	print 'colors:', ug[1416], gr[1416], ri[1416], iz[1416]
	print 'r magnitude:',r[1416]
	print 'Comment:NONE'
	
plt.figtext(0.04 ,.02, u'NSAID: 141119\nIAU Name: J121857.50+471813.9\nRA: 184.739610145\nDec: 47.3039712546\nDflags: [64 64  0  0  0  0  0]\nRadius: 98.8767\ncolors:[0.506425, 1.63258, 1.49803, 0.734675]\nr magnitude: 10.6451\nComment:NONE')
plt.suptitle('NGC 4258',size=18)
plt.show()