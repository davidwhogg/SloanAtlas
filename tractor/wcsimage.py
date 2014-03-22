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

def wcsimage(name, iauname, mean=False, direc='RC3_Output'):
    CG = unpickle_from_file("%s/%s.pickle" %(direc,name))
    table = pyfits.open('sdss_atlas_plates_quants.fits')[1].data
    h50i = table['CG_H50S'][:,3]
    h90i = table['CG_H90S'][:,3]
    names = table['NAME']
    fn = '%s_SA_%s-i.fits.gz' %(name, iauname)

    if not os.path.exists(fn):
        cmd = "scp ep109@bootes.cosmo.fas.nyu.edu:/global/data/scr/dwh3/ep109/all_images/" + fn + " ."
        print cmd
        os.system(cmd)
    
    f = pyfits.open(fn)

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
    model = mimgs[3]
    plt.imshow(data-mimgs[3], origin ='lower',cmap=matplotlib.cm.Greys, vmin=vmin, vmax=vmax)
    plt.xlim(4*len(mimgs[3])/9, 5*len(mimgs[3])/9)
    plt.ylim(4*len(mimgs[3])/9, 5*len(mimgs[3])/9)
    plt.title('difference')
    plt.tight_layout()
    plt.savefig('%s_data_wcs.pdf' %(name))
    
    if mean:
        
        r50s = []
        r90s = []
        concs = []
        h50s =[]
        h90s = [] 
        expr50 = CG.shapeExp.re * np.sqrt(CG.shapeExp.ab)
        devr50 = CG.shapeDev.re * np.sqrt(CG.shapeDev.ab)
        yg, xg = np.meshgrid(np.arange(imageh) - crpix2, np.arange(imagew) - crpix1)
        r2g = xg ** 2 + yg ** 2
        rlist_pix = np.exp(np.linspace(0.,np.log(0.5*imageh),64))
        rlist_arcsec = rlist_pix * pixscale * 3600.

        betamin = 0
        betabin = 0.1
        betamax = 1 + betabin
        betas = np.arange(betamin,betamax,betabin)
        print betas
        model = np.array(model)
        for beta in betas:
            
            dm = (data ** beta) * (model ** (1-beta))
            image = dm
            bad = np.where(np.logical_not(np.isfinite(image)))
            image[bad] = 0.
            # make variance tensor out of image; get principal eigenvector
            foo = np.sum(image * xg * yg)
            V = np.array([[np.sum(image * xg * xg), foo],
                          [foo, np.sum(image * yg * yg)]])
            u, v = np.linalg.eig(V) 
            #print v[np.argmax(u)], v[:,np.argmax(u)], u
            principal_vector = v[:,np.argmax(u)].reshape((2,)) 
            assert (np.dot(principal_vector, principal_vector) - 1.) < 1e-8

            # do rectangular integrals on "diagonals"
            rdotv = xg * principal_vector[0] + yg * principal_vector[1]
            hlist = [np.sum(image[np.abs(rdotv) < r]) for r in rlist_pix]
            hlist /= hlist[-1]
            h50, h90 = np.interp([0.5,0.9],hlist, rlist_arcsec)
            h50s.append(h50)
            h90s.append(h90)
            print h50, h90, 'h50 h90'

            # do circular integrals
            # plist = [np.sum(image[r2g < (r * r)]) for r in rlist_pix]
            # plist /= plist[-1]
            # r50, r90 = np.interp([0.5, 0.9], plist, rlist_arcsec)
            # conc = r90/r50
            # r50s.append(r50)
            # r90s.append(r90)
            # concs.append(conc)
            # print r50, r90, 'r50','r90'

        plt.figure()
        plt.subplot(121)
        plt.plot(betas, h50s)
        for i in range(len(names)):
            if names[i] == name.replace('_',' '): 
                plt.axhline(h50i[i], c='r', ls='--')
        plt.title('h50')
        plt.subplot(122)
        plt.plot(betas,h90s)
        for i in range(len(names)):
            if names[i] == name.replace('_',' '): 
                plt.axhline(h90i[i], c='r', ls='--')
        plt.title('h90')
        plt.suptitle('%s' %(name))
        plt.savefig('geometric_mean_%s.pdf' %(name))
    return 'done'

    
if __name__ == "__main__":
    #wcsimage('NGC_4736','J125053.00+410712.4', mean=True)
    #wcsimage('NGC_3377','J104742.33+135909.3', mean=True)
    #edgeons
    wcsimage('NGC_4710','J124938.83+150956.6', mean=True)
    wcsimage('NGC_4771','J125321.24+011608.3', mean=True)
    wcsimage('NGC_2862','J092455.09+264629.9', mean=True)
    wcsimage('NGC_3126','J100820.70+315146.9', mean=True)
    wcsimage('UGC_7170','J121036.85+184926.6', mean=True)
