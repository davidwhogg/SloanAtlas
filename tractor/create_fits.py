import numpy as np
import pyfits as pyf
import os
import sys
from tractor.rc3 import *
from astrometry.util.file import *
from astrometry.util.starutil_numpy import *
from astrometry.util.degtohms import *
import matplotlib
import pylab as plt
from astropysics.obstools import *

def sb(i,r):
    return i + 2.5*log10(2) + 2.5*log10(pi*r**2)

def extinction(pos):
    #pos=ra,dec
    sloanu=5.155
    sloang=3.793
    sloanr=2.751
    sloani=2.086
    sloanz=1.479

    galactic=radectolb(pos[0],pos[1])
    x=get_SFD_dust(galactic[0], galactic[1],dustmap='ebv',interpolate=True)
    extinction_all=[x*sloanu,x*sloang,x*sloanr,x*sloani,x*sloanz]
    extu=float(extinction_all[0])
    extg=float(extinction_all[1])
    extr=float(extinction_all[2])
    exti=float(extinction_all[3])
    extz=float(extinction_all[4])
    return extu,extg,extr,exti,extz

def iauname(ra,dec):
    rastring = ra2hmsstring(ra, separator='')[:9]
    decstring =  dec2dmsstring(dec,separator='')[:9]
    iau = 'SA J{}'.format(rastring + decstring)
    return iau

def makegeneraltable(fn):
    iaus = []
    names = []
    cg_ra=[]
    cg_dec=[]
    cg_totmags=[]
    cg_devmags=[]
    cg_devre=[]
    cg_devab=[]
    cg_devphi=[]
    cg_expmags=[]
    cg_expre=[]
    cg_expab=[]
    cg_expphi=[]
    cg_r50s=[]
    cg_r90s=[]
    cg_h50s=[]
    cg_h90s=[]
    cg_extinction=[]
    cg_sb=[]
    cg_hsb=[]

    directories =["swapped/pickles/","NSAtlas_Output", "RC3_Output/"]
    for direc in directories:
        print direc
        for files in os.listdir(direc):
            if files.endswith("-updated2.pickle"):
                #print files
                strip=files.split('-u')
                name=strip[0].replace('_',' ')
                if name in names:
                    print 'THIS GALAXY ALREADY HAS A SWAPPED ENTRY, SKIPPING'
                    continue
            
                names.append(name)
                print name
                CG,r50s,r90s,concs, h50s, h90s=unpickle_from_file('%s/%s' %(direc,files))
                pos=CG.getPosition()
                tot=CG.getBrightness()
                iau = iauname(pos[0],pos[1])
                print iau
                iaus.append(iau)
                cg_ra.append(pos[0])
                cg_dec.append(pos[1])
                cg_r50s.append(r50s)
                cg_r90s.append(r90s)
                cg_totmags.append(tot)
                cg_devmags.append(CG.brightnessDev)
                cg_devre.append(CG.shapeDev.re)
                cg_devab.append(CG.shapeDev.ab)
                cg_devphi.append(CG.shapeDev.phi)
                cg_expmags.append(CG.brightnessExp)
                cg_expre.append(CG.shapeExp.re)
                cg_expab.append(CG.shapeExp.ab)
                cg_expphi.append(CG.shapeExp.phi)
                cg_h50s.append(h50s)
                cg_h90s.append(h90s)

                #get extinction from SFD
                cg_extinction.append(extinction(pos))

                #calculate sb twice
                imag_corrected = tot[3]-extinction(pos)[3]
                cg_sb.append(sb(imag_corrected,r50s[3]))
                cg_hsb.append(sb(imag_corrected,h50s[3]))

    #now have all data to write to fits file   
    n=np.arange(100)
    hdu=pyf.PrimaryHDU(n)
    col1= pyf.Column(name='NAME',format='30A',array=np.array(names))
    col2= pyf.Column(name='IAU_NAME',format='30A',array=np.array(iaus))
    col3= pyf.Column(name='CG_RA',format='1E',array=np.array(cg_ra))
    col4= pyf.Column(name='CG_DEC',format='1E',array=np.array(cg_dec))
    col5= pyf.Column(name='CG_R50S',format='5E',array=np.array(r50s))
    col6= pyf.Column(name='CG_R90S',format='5E',array=np.array(r90s))
    col7= pyf.Column(name='CG_TOTMAGS',format='5E',array=np.array(cg_totmags))
    col8= pyf.Column(name='CG_DEVRE',format='1E',array=np.array(cg_devre))
    col9= pyf.Column(name='CG_DEVAB',format='1E',array=np.array(cg_devab))
    col10=pyf.Column(name='CG_DEVPHI',format='1E',array=np.array(cg_devphi))
    col11=pyf.Column(name='CG_DEVMAGS',format='5E',array=np.array(cg_devmags))
    col12=pyf.Column(name='CG_EXPRE',format='1E',array=np.array(cg_expre))
    col13=pyf.Column(name='CG_EXPAB',format='1E',array=np.array(cg_expab))
    col14=pyf.Column(name='CG_EXPPHI',format='1E',array=np.array(cg_expphi))
    col15=pyf.Column(name='CG_EXPMAGS',format='5E',array=np.array(cg_expmags))
    col16=pyf.Column(name='CG_EXTINCTION',format='5E',array=np.array(cg_extinction))
    col17=pyf.Column(name='CG_SB', format='1E',array=np.array(cg_sb))
    col18=pyf.Column(name='CG_HSB', format='1E',array=np.array(cg_hsb))
    col19=pyf.Column(name='CG_H50S', format='5E', array=np.array(cg_h50s))
    col20=pyf.Column(name='CG_H90S', format='5E', array=np.array(cg_h90s))
    cols=pyf.ColDefs([col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14,col15,col16,col17,col18,col19,col20])
    tbhdu=pyf.new_table(cols)
    tbhdulist=pyf.HDUList([hdu,tbhdu])
    tbhdulist.writeto(fn,clobber=True)
    return tbhdulist

def sorttable(fn, column, newfn):
    '''fn: fits file to be sorted
       column: column to sort on
       newfn: new fits file name to be saved'''

    tabledata = pyf.open(fn)[1].data
    sortparam = np.argsort(tabledata.field(column)[:,3]) #[:,3] refers to i-band for properties with all ugriz values
    print sortparam
    newtable = tabledata[sortparam]
    hdu = pyf.BinTableHDU(newtable)
    hdu.writeto(newfn, clobber=True)
    return '%s made' %newfn

def cuttable(fn, column, value, newfn):
    '''fn: fits file to be sorted
       column: column to sort on
       value: the lower limit of the value that the data will be cut on
       newfn: new fits file name to be saved'''
    tabledata = pyf.open(fn)[1].data
    mask = tabledata.field(column)[:,3]
    newtable = tabledata[mask]
    hdu = pyf.BinTableHDU(newtable)
    hdu.writeto(newfn, clobber=True)
    return '%s made' %newfn

if __name__ == '__main__':
    makegeneraltable('SA_master_2014.fits')
    sorttable('SA_master_2014.fits', 'CG_H50S','SA_master_2014_sorted.fits')
