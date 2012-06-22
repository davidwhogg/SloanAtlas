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
    

21448
26781
31572
37123
42502
45162
50644
56347
61396
65970
67938
72627
78212
83532
89205
print g[200]
print g[250]
print g[300]
print g[350]
print g[400]
print g[450]
print g[500]
print g[550]
print g[600]
print g[650]
print g[700]
print g[750]
print g[800]
print g[850]
print g[900]