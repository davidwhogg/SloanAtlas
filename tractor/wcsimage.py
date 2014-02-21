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

matplotlib.rcParams.update({'font.size': 10})

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

    tan = Tan(crval1,crval2,crpix1,crpix2,cd11,cd12,cd21,cd22,imagew,imageh)
    print tan

    wcs = ba.FitsWcs(tan)
    print wcs

    data=np.zeros((imagew,imageh))
    invvar=np.ones((imagew,imageh))
    psf = ba.GaussianMixturePSF(1.,[0.,0.],np.array(1.)) #amp,mean,var
    skyobj = ba.ConstantSky(0.)
    zr = np.array([-5.,+5.])
    pixscale = np.sqrt(np.abs(cd11 * cd22 - cd12 * cd21))
    
    tims = []
    bands = ['u','g','r','i','z']
    for bandname in bands:
        photocal = st.SdssNanomaggiesPhotoCal(bandname)
#        photocal.zeropoint += 2.5 * np.log10(4.)
        photocal.zeropoint += 5. * np.log10(0.396 / 3600. / pixscale)
        image = en.Image(data=data,invvar=invvar,sky=skyobj,psf=psf,wcs=wcs,photocal=photocal,name="Half-light %s" %bandname,zr=zr)
        tims.append(image)
    
    tractor = st.SDSSTractor(tims)
    tractor.addSources([CG])
    mimgs = tractor.getModelImages()

    plt.figure()    
    plt.subplot(132)
    print np.min(mimgs[3])
    print np.max(mimgs[3])
    print mimgs[3].shape
    vmin = - 0.125 * np.max(mimgs[3])
    vmax = 0.
    plt.imshow(-mimgs[3], origin='lower',cmap=matplotlib.cm.Greys, vmin=vmin, vmax=vmax)
    plt.xlim(4*len(mimgs[3])/9, 5*len(mimgs[3])/9)
    plt.ylim(4*len(mimgs[3])/9, 5*len(mimgs[3])/9)
    plt.title('synthetic')
    plt.suptitle('%s, original dimensions:%s,%s' %(name, imagew, imageh))
    xlim = plt.xlim()
    ylim = plt.ylim()
    

    plt.subplot(131)
    data = f[0].data
    print np.min(data)
    print np.max(data)
    print data.shape
    plt.imshow(-data, origin='lower',cmap=matplotlib.cm.Greys, vmin=vmin, vmax=vmax)
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.title('data')

    plt.subplot(133)
    vmin = -0.0625 * np.max(mimgs[3])
    vmax = -vmin
    plt.imshow(data-mimgs[3], origin ='lower',cmap=matplotlib.cm.Greys, vmin=vmin, vmax=vmax)
    plt.xlim(4*len(mimgs[3])/9, 5*len(mimgs[3])/9)
    plt.ylim(4*len(mimgs[3])/9, 5*len(mimgs[3])/9)
    plt.title('difference')
    plt.tight_layout()
    plt.savefig('%s_data_wcs.pdf' %(name))

    return 'done'

if __name__ == "__main__":
    wcsimage('NGC_4736','J125053.00+410712.4')
    wcsimage('NGC_3377','J104742.33+135909.3')
