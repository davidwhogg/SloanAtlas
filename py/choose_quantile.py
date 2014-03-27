import numpy as np
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text', usetex=True)
import matplotlib.pyplot
import pylab as plt
from pylab import *
import pyfits as pyf
from astropysics.obstools import *
import os
import astropy.io.fits as fits
from astropy.table import Column

def openfile(fn):
    '''returns HDUtable'''
    return pyf.open('%s.fits' %(fn))

def openfile_data(fn):
    '''returns rows of data'''
    hdulist=openfile(fn)
    return hdulist[1].data

def quantiles(x,q):
    '''returns data value for the element in the list that its being cut on'''
    sortedx=sorted(x)    
    if q == 1.0:
        qval=sortedx[len(sortedx)-1]
    else:
        qval=sortedx[int(q*len(sortedx))]   
    return qval

def choose_quantiles(ncolor, nsb):
    '''
    inputs:
    ncolor is the number of color bins
    nsb is the number of sb bins
    
    outputs: 
    given a data table and the number of bins desired in
    color and sb, a quantile is assigned to each galaxy in the range
    ncolor x nsb. a colors vs. sb plot indicating the breakdown of
    quantiles is also generated.
    '''
    table = openfile_data('sdss_atlas_plates') #sdss_atlas_sept2013')    
    extinction = table['CG_EXTINCTION']
    surface_bright = table['CG_I-SB']
    mags = table['CG_TOTMAGS']
    radii = table['CG_R50S'][:,3]
    g = mags[:,1]-extinction[:,1]
    i = mags[:,3]-extinction[:,3]
    gi = g-i
    colors = gi
    sbs = surface_bright
    quantile_list = np.zeros(len(sbs)).astype(int) - 1

    #scatter plot whole table
    plt.figure()
    plt.plot(colors,sbs, 'k.', alpha=0.5)

    ncolor = ncolor
    nsb = nsb
    nsubsample = ncolor * nsb
    hquants = np.arange(1./ncolor, 0.999, 1./ncolor)
    vquants = np.arange(1./nsb, 0.999, 1./nsb)

    hqvalue = []     
    for i in hquants:
        #print i
        hqvalue.append(quantiles(colors, i))    
    # put upper and low bounds on colors/sb to avoid extreme outliers
    color50 = quantiles(colors,0.5)
    hqvalue.insert(0,color50+1.5*(quantiles(colors,0.025)-color50))
    hqvalue.append(color50+1.5*(quantiles(colors,0.975)-color50))
    sb50 = quantiles(sbs,0.5)
    vqlo = sb50 + 1.5*(quantiles(sbs,0.025) - sb50)
    vqhi = sb50 + 1.5*(quantiles(sbs,0.975) - sb50)
    
    #create bounds
    colorlo = np.zeros(nsubsample)
    colorhi = np.zeros(nsubsample)
    sblo = np.zeros(nsubsample)
    sbhi = np.zeros(nsubsample)
    k = 0
    for i in range(ncolor):
        I = (colors > hqvalue[i]) * (colors < hqvalue[i+1])
        sample = table[I]
        sample_sb = sample['CG_I-SB']
        foo = np.zeros(nsb + 1)
        foo[0] = vqlo
        foo[nsb] = vqhi
        for j in range(nsb):
            if (j + 1) < nsb:
                foo[j + 1]= quantiles(sample_sb, vquants[j])
            k = j + i * nsb
            print k 
            assert colorlo[k] == 0.
            colorlo[k] = hqvalue[i]
            colorhi[k] = hqvalue[i+1]
            sblo[k] = foo[j]
            sbhi[k] = foo[j+1]
            plt.vlines(hqvalue[i], ymin=sblo[k], ymax=sbhi[k])
            plt.hlines(foo[j], xmin=colorlo[k], xmax=colorhi[k])
    plt.xlim(hqvalue[0], hqvalue[len(hqvalue)-1])
    plt.ylim(vqlo,vqhi)

    #assign quantile number
    for k in range(nsubsample):
        I = (colors > colorlo[k]) * (colors < colorhi[k]) * (sbs > sblo[k]) * (sbs < sbhi[k])
        quantile_list[I] = k
    assert np.all(quantiles >= 0)
    #print len(quantile_list), quantile_list
    #plt.savefig('choose_quantiles5_3.pdf')
    #os.system('cp choose_quantiles5_3.pdf ~/public_html')
    make_quantile_table(table, quantile_list)
    return 'done'

def make_quantile_table(data, quantile_list):
    ''' 
    inputs:
    existing table and a list of quantiles for each galaxy
    
    outputs:
    a new data table to be used for the creation of quantile webpages
    '''

    n=np.arange(100)
    hdu=pyf.PrimaryHDU(n)    
    col1=pyf.Column(name='NAME', format='30A', array=data['NAME'])
    col2=pyf.Column(name='CG_RA',format='1E',array=data['CG_RA'])
    col3=pyf.Column(name='CG_DEC',format='1E',array=data['CG_DEC'])
    col4=pyf.Column(name='CG_R50S',format='5E',array=data['CG_R50S'])
    col5=pyf.Column(name='CG_R90S',format='5E',array=data['CG_R90S'])
    col6=pyf.Column(name='CG_TOTMAGS',format='5E',array=data['CG_TOTMAGS'])
    col7=pyf.Column(name='CG_EXTINCTION',format='5E',array=data['CG_EXTINCTION'])
    col8=pyf.Column(name='CG_ISB', format='1E',array=data['CG_ISB'])
    col9=pyf.Column(name='QUANTILE',format='1E',array=quantile_list)
    col10=pyf.Column(name='CG_H50S',format='5E', array=data['CG_H50S'])
    col11=pyf.Column(name='CG_H90S', format='5E', array=data['CG_H90S'])
    cols=col1,col2,col3,col4,col5,col6,col7,col8,col9,col10, col11
    tbhdu=pyf.new_table(cols)
    tbhdulist=pyf.HDUList([hdu,tbhdu])
    tbhdulist.writeto('sdss_atlas_plates_quants.fits', clobber=True) #'sdss_atlas_for_images_all.fits',clobber=True)

if __name__ == '__main__':    
    choose_quantiles(5, 3)
   
    
