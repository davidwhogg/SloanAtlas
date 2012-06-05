#creates the triangle comparison plot with stars placed for the specified galaxy
import matplotlib
import numpy as np
import pylab as plt
import pyfits as pyf

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    a=data.field('RA')
    b=data.field('DEC')
    e=data.field('NSAID')
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
k = 0
x=[757,1882,643,393,758,1879,256,352,2035,1018,445,40,722,1982,1832,1335]
for t in x:
	k += 1
	plt.figure(figsize=(8,8))
	plt.subplots_adjust(wspace=0,hspace=0)
	matplotlib.rcParams['font.size'] = 9

	plt.subplot(551)
	plt.plot(badug,badsersic,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(-0.5,2.1)
	plt.ylim(0.5,6.1)
	plt.xlabel(r"$u-g$")
	plt.ylabel('n')
	plt.plot(ug[t],sersic[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(552)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badgr,badsersic,'m.',alpha=0.5,ms=1.5)
	plt.plot(gr,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,4)
	plt.ylim(0.5,6.1)
	plt.xlabel(r"$g-r$")
	plt.plot(gr[t],sersic[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(553)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badri,badsersic,'m.',alpha=0.5,ms=1.5)
	plt.plot(ri,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0.5,2.1)
	plt.ylim(0.5,6.1)
	plt.xlabel(r"$r-i$")
	plt.plot(ri[t],sersic[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(554)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badiz,badsersic,'k.',alpha=0.5,ms=1.5)
	plt.plot(iz,sersic,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,1.2)
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
	plt.xlim(-0.5,2.1)
	plt.ylim(17,24)
	plt.yticks([18,20,22,24],[18,20,22,24])
	plt.xlabel(r"$u-g$")
	plt.ylabel(r"$\mu_i$")
	plt.plot(ug[t],sb[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(557)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badgr,badsb,'m.',alpha=0.5,ms=1.5)
	plt.plot(gr,sb,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,4)
	plt.ylim(17,24)
	plt.xlabel(r"$g-r$")
	plt.plot(gr[t],sb[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(558)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badri,badsb,'m.',alpha=0.5,ms=1.5)
	plt.plot(ri,sb,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0.5,2.1)
	plt.ylim(17,24)
	plt.xlabel(r"$r-i$")
	plt.plot(ri[t],sb[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(559)
	plt.tick_params(axis='both',labelleft='off')
	plt.plot(badiz,badsb,'k.',alpha=0.5,ms=1.5)
	plt.plot(iz,sb,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,1.2)
	plt.xticks([.2,.4,.6,.8,1.0],[.2,.4,.6,.8,1.0])
	plt.ylim(17,24)
	plt.xlabel(r"$i-z$")
	plt.plot(iz[t],sb[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,11)
	plt.plot(badug,badiz,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,iz,'k.',alpha=0.5,ms=1.5)
	plt.xlim(-0.5,2.1)
	plt.ylim(0,1.2)
	plt.yticks([0.2,0.4,0.6,0.8,1.0],[0.2,0.4,0.6,0.8,1.0])
	plt.xlabel(r"$u-g$")
	plt.ylabel(r"$i-z$")
	plt.plot(ug[t],iz[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,12)
	plt.tick_params(axis='both',labelbottom='off',labelleft='off')
	plt.plot(badgr,badiz,'m.',alpha=0.5,ms=1.5)
	plt.plot(gr,iz,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0,4)
	plt.ylim(0,1.2)
	plt.xlabel(r"$g-r$")
	plt.plot(gr[t],iz[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,13)
	plt.tick_params(axis='both',labelleft='off')
	plt.plot(badri,badiz,'m.',alpha=0.5,ms=1.5)
	plt.plot(ri,iz,'k.',alpha=0.5,ms=1.5)
	plt.xlim(0.5,2.1)
	plt.xticks([0.5,1.0,1.5,2.0],[0.5,1.0,1.5,2.0])
	plt.ylim(0,1.2)
	plt.xlabel(r"$r-i$")
	plt.plot(ri[t],iz[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,16)
	plt.plot(badug,badri,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,ri,'k.',alpha=0.5,ms=1.5)
	plt.xlim(-0.5,2.1)
	plt.ylim(0.5,2.1)
	plt.yticks([0.8,1.0,1.2,1.4,1.6,1.8],[0.8,1.0,1.2,1.4,1.6,1.8])
	plt.xlabel(r"$u-g$")
	plt.ylabel(r"$r-i$")
	plt.plot(ug[t],ri[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,17)
	plt.tick_params(axis='both',labelleft='off')
	plt.plot(badgr,badri,'m.',alpha=0.5,ms=1.5)
	plt.plot(gr,ri,'k.',alpha=0.5,ms=1.5)		
	plt.xlim(0,4)
	plt.xticks([0.5,1.5,2.5,3.5],[0.5,1.5,2.5,3.5])
	plt.ylim(0.5,2.1)
	plt.xlabel(r"$g-r$")
	plt.plot(gr[t],ri[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')

	plt.subplot(5,5,21)
	plt.plot(badug,badgr,'m.',alpha=0.5,ms=1.5)
	plt.plot(ug,gr,'k.',alpha=0.5,ms=1.5)
	plt.xlim(-0.5,2.1)
	plt.xlabel(r"$u-g$")
	plt.yticks([0.5,1.5,2.5,3.5],[0.5,1.5,2.5,3.5])
	plt.ylim(0,4)
	plt.ylabel(r"$g-r$")
	plt.plot(ug[t],gr[t],'*',ms=9,markeredgecolor='red',markeredgewidth=0.9,markerfacecolor='none')
	plt.suptitle('%s' % e[good][t]) 
	plt.savefig('exemplar%2d_plot3.pdf' % k) 
	#plt.show()