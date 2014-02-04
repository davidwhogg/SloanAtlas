if __name__ == '__main__':
    import matplotlib
    matplotlib.use('Agg')

import os
import logging
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab as plt
import Image
import pyfits

from astrometry.util.file import *

from tractor import *
from tractor import sdss as st
from tractor.saveImg import *
from tractor import sdss_galaxy as sg
from tractor import basics as ba
from tractor import engine as en
from astrometry.util.util import Tan
from tractor.emfit import em_fit_2d
from tractor.fitpsf import em_init_params


f = pyfits.open('NGC_3377_SA_J104742.33+135909.3-i.fits')
#print f[0].header
data = f[1].data
#print data[2].shape


def wcsimage(name, iauname, direc='RC3_Output'):
    CG = unpickle_from_file("%s/%s.pickle" %(direc,name))
    # ra,dec = CG.getPosition()
    # maxradius=max(CG.shapeExp.re,CG.shapeDev.re)
    # print "Working on %s" % name
    # print CG
    # assert(maxradius<500.)
    
    f = pyfits.open('%s_SA_%s-i.fits' %(name, iauname))

    crval1 = f[0].header['CRVAL1']
    crval2 = f[0].header['CRVAL2']
    crpix1 = f[0].header['CRPIX1'] 
    crpix2 = f[0].header['CRPIX2']
    cd11 = f[0].header['CD1_1'] 
    cd12 = f[0].header['CD1_2'] 
    cd21 = f[0].header['CD2_1'] 
    cd22 = f[0].header['CD2_2'] 
    imagew = f[0].header['NAXIS1'] 
    imageh = f[0].header['NAXIS2']
    print crval1, crval2, crpix1, crpix2, cd11, cd12,cd21,cd22, imagew, imageh
    pixscale = cd11

    tan = Tan(crval1,crval2,crpix1,crpix2,cd11,cd12,cd21,cd22,imagew,imageh)
    print tan

    wcs = ba.FitsWcs(tan)
    print wcs

    data=np.zeros((imagew,imageh))
    invvar=np.ones((imagew,imageh))
    psf = ba.GaussianMixturePSF(1.,[0.,0.],np.array(1.)) #amp,mean,var
    skyobj = ba.ConstantSky(0.)
    zr = np.array([-5.,+5.])
    
    tims = []
    bands = ['u','g','r','i','z']
    for bandname in bands:
        photocal = st.SdssNanomaggiesPhotoCal(bandname)
        image = en.Image(data=data,invvar=invvar,sky=skyobj,psf=psf,wcs=wcs,photocal=photocal,name="Half-light %s" %bandname,zr=zr)
        tims.append(image)
    
    tractor = st.SDSSTractor(tims)
    tractor.addSources([CG])
    mimgs = tractor.getModelImages()

    plt.figure()    
    plt.subplot(122)
    print np.min(mimgs[3]) 
    print mimgs[3].shape
    plt.imshow(mimgs[3], origin='lower',cmap=matplotlib.cm.Greys, vmin=np.min(mimgs[3]), vmax=np.max(mimgs[3]))
    plt.xlim(4*len(mimgs[3])/9, 5*len(mimgs[3])/9)
    plt.ylim(4*len(mimgs[3])/9, 5*len(mimgs[3])/9)
    plt.title('synthetic')
    plt.suptitle('%s, original dimensions:%s,%s' %(name, imagew, imageh))
    

    plt.subplot(121)
    data = f[1].data
    print len(data)
    plt.imshow(data, cmap=matplotlib.cm.Greys, vmin=np.min(mimgs[3]), vmax=np.max(mimgs[3]))
    plt.xlim(4*len(data)/9, 5*len(data)/9)
    plt.ylim(4*len(data)/9, 5*len(data)/9)
    plt.title('data')
    plt.savefig('%s_data_wcs.pdf' %(name))

    return 'done'

wcsimage('NGC_4736','J125053.00+410712.4')
wcsimage('NGC_3377','J104742.33+135909.3')
