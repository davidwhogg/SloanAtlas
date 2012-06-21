import matplotlib
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



plt.plot(badgr,badri,'m.', alpha=0.5)
plt.plot(gr, ri,'k.', alpha=0.5)
plt.xlabel(r"$g-r$")
plt.ylabel(r"$r-i$")
plt.plot(.6319,.3614,'*',ms=12,markeredgecolor='red',markeredgewidth=1,markerfacecolor='none', label='175')
plt.plot(0.5938,.3541,'*',ms=12,markeredgecolor='yellow',markeredgewidth=1,markerfacecolor='none', label='3338')
plt.plot(0.7385,0.43180,'*',ms=12,markeredgecolor='cyan',markeredgewidth=1,markerfacecolor='none', label='4148')
plt.plot(0.792,0.4623,'*',ms=12,markeredgecolor='green',markeredgewidth=1,markerfacecolor='none', label='4217')
plt.plot(.8657,.4770,'*',ms=12,markeredgecolor='blue',markeredgewidth=1,markerfacecolor='none', label='741')
#plt.plot(,'*',ms=12,markeredgecolor='blue',markeredgewidth=1,markerfacecolor='none', label='4258')
# RUN 4258 successfully and add in color marker
plt.xlim(0,1.2)
plt.ylim(-.1,0.8)
plt.legend(loc='lower right')
plt.savefig('colorplotcomparison.pdf')


plt.show()
