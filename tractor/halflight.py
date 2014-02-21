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

def halflight(name,makePlots=False,images=False,direc='RC3_Output'):
    CG = unpickle_from_file("%s/%s.pickle" %(direc,name))
    ra,dec = CG.getPosition()
    maxradius=max(CG.shapeExp.re,CG.shapeDev.re)
    print "Working on %s" % name
    #print CG

    # if maxradius > 500.:
    #     f=open('cannot_be_pickled.txt','a')
    #     f.write(name)
    #     continue
    assert(maxradius<500.)
    
    #First step is to make an image, which needs:
    # data, invvar, psf, wcs, sky, photocal, name, zr
    
    crval1 = ra
    crval2 = dec
    pixscale = cd11 = .396/3600.
    cd12 = 0.
    cd21 = 0.
    cd22 = pixscale
    imagew = int(32*maxradius)
    crpix1 = .5*imagew
    imageh = int(32*maxradius)
    crpix2 = .5*imageh
    tan = Tan(crval1,crval2,crpix1,crpix2,cd11,cd12,cd21,cd22,imagew,imageh)

    wcs = ba.FitsWcs(tan)

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

    yg, xg = np.meshgrid(np.arange(imageh) - crpix2, np.arange(imagew) - crpix1)
    r2g = xg ** 2 + yg ** 2
    rlist_pix = np.exp(np.linspace(0.,np.log(0.5*imageh),64))
    rlist_arcsec = rlist_pix * pixscale * 3600.
    mimgs = tractor.getModelImages()
 
    r50s = []
    r90s = []
    concs = []
    h50s =[]
    h90s = [] 
    expr50 = CG.shapeExp.re * np.sqrt(CG.shapeExp.ab)
    devr50 = CG.shapeDev.re * np.sqrt(CG.shapeDev.ab)

    for bandname,image in zip(bands,mimgs):
        # do circular integrals
        plist = [np.sum(image[r2g < (r * r)]) for r in rlist_pix]

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

        # check that hlist "makes sense" relative to plist
        # print hlist, plist
        # bins=np.arange(0,64,1.)
        # plt.plot(bins,hlist,label='rectangular')
        # plt.plot(bins,plist,label='circular')
        # plt.legend(loc='upper left')
        # plt.savefig('hplist.pdf')

        plist /= plist[-1]
        r50, r90 = np.interp([0.5, 0.9], plist, rlist_arcsec)
        print r50,r90
        conc = r90/r50
        r50s.append(r50)
        r90s.append(r90)
        concs.append(conc)
        if r50<min(devr50,expr50) or r50>max(devr50,expr50):
            print "R50 is not in between DeV and exp radii for %s" %name
        if 1./conc > .46 or 1./conc <.29:
            print "C=%.2f is a strange concentration for %s" % (conc,name)
        print name, bandname, r50, r90, conc

        if images:
            if bandname=='i':
                print principal_vector #might need to flip y-coordinate
                plt.figure()
                plt.imshow(image,cmap=matplotlib.cm.gray, vmin=0, vmax=0.05*np.max(image))
                plt.savefig('%s_%s.png' %(name, bandname))
                print 'plotted image'
                plt.figure()
                plt.clf()
                plt.imshow(np.abs(rdotv), cmap=matplotlib.cm.gray)
                plt.savefig('rdotv_%s_%s.png' %(name,bandname))

        if makePlots:
            plt.clf()
            plt.axhline(0,color='k',alpha=0.25)
            plt.xlabel("radius in arcsecond")
            plt.ylabel("fraction of azimuthally averaged flux")
            plt.title("%s" %name)
            plt.plot(rlist_arcsec, plist, 'k-')
            plt.axvline(r50, color='k', alpha=0.5)
            plt.axvline(r90, color='k', alpha=0.5)
            plt.axvline(devr50, color='r', alpha=0.5)
            plt.axvline(expr50, color='b', alpha=0.5)
            plt.text(1.02 * r90, 0.01, "$C = %.1f$" % (conc), ha='left')
            plt.xlim(0,2.*r90)
            plt.ylim(-0.1,1.1)
            plt.savefig("radial-profile-%s-%s.png" % (name,bandname))

    pickle_to_file([CG,r50s,r90s,concs, h50s, h90s],'%s/%s-updated2.pickle' %(direc,name))


def main():
    import optparse
    parser = optparse.OptionParser(usage='%prog [options] <name>')
    opt,args = parser.parse_args()
    if len(args) != 1:
        parser.print_help()
        sys.exit(-1)

    name = args[0]
    halflight(name)

if __name__ == '__main__':
    main()
