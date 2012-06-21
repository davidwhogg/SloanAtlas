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