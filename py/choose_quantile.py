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
    table = openfile_data('sdss_atlas_sept2013')    
    extinction = table['CG_EXTINCTION']
    surface_bright = table['CG_I-SB']
    mags = table['CG_TOTMAGS']
    radii = table['CG_R50S'][:,3]
    g = mags[:,1]-extinction[:,1]
    i = mags[:,3]-extinction[:,3]
    gi = g-i
    colors = gi
    sbs = surface_bright
    
    #scatter plot whole table
    plt.figure()
    plt.plot(colors,sbs, 'k.', alpha=0.5)

    ncolor = ncolor
    nsb = nsb
    colorbin = 1./ncolor
    hquants = np.arange(colorbin, 1, colorbin)
    hqs = list(hquants)
    
    hqvalue = []     
    for i in hqs:
        #print i
        hqvalue.append(quantiles(colors, i))    
    # put upper and low bounds on colors to avoid extreme outliers
    hqvalue.insert(0,quantiles(colors,0.5)+1.5*(quantiles(colors,0.025)-quantiles(colors,0.5)))
    hqvalue.append(quantiles(colors,0.5)+1.5*(quantiles(colors,0.975)-quantiles(colors,0.5)))
    
    sbbin = 1./nsb
    vquants = np.arange(sbbin, 0.99, sbbin)
    vqs = list(vquants)
    vqvalue = []
    for j in vqs:
        print j
        for i in range(ncolor):
            I = (colors > hqvalue[i]) * (colors < hqvalue[i+1])
            sample = table[I]
            sample_sb = sample['CG_I-SB']
            vqvalue.append(quantiles(sample_sb, j))

    #group the values for each of the sb cuts together, i.e. all 25th percentile lines, then all 50th percentile lines, etc.
    chunks=[vqvalue[x:x+(len(hqvalue)-1)] for x in xrange(0, len(vqvalue), len(hqvalue)-1)]
    
    #create plot limits, restrictions are color50 + 1.5(color2.5 - color50) and color50+1.5(color97.5-color50), same for sb
    sb50 = quantiles(surface_bright,0.5)
    minsb = sb50 + 1.5*(quantiles(surface_bright,0.025) - sb50)
    maxsb = sb50 + 1.5*(quantiles(surface_bright,0.975) - sb50)
    print vquants,vqvalue
    plt.xlim(hqvalue[0], hqvalue[len(hqvalue)-1])
    plt.ylim(minsb, maxsb)

    #plot vertical colors lines
    for vline in hqvalue:
        plt.vlines(vline, ymin=minsb, ymax=maxsb)
        
    #plot horizontal sb lines
    for i in chunks:
        for j,k in zip(i, range(len(hqvalue))):
            #print j, hqvalue[k], hqvalue[k+1]
            plt.hlines(j, xmin=hqvalue[k], xmax=hqvalue[k+1])

    #assign quantile numbers to each galaxy
    datasets = []
    quantile_list =[]

    #break the dataset into ncolor data masks
    for j in range(ncolor):
        datasets.append(table[(colors > hqvalue[j]) * (colors < hqvalue[j+1])])
    print len(datasets)
    print datasets[0]
    assert False

    #break each data mask into nsb bins each, total = ncolor x nsb bins
    all_sets =[]
    vquants = list(vquants)
    vquants.insert(0,0)
    vquants.append(1.)    
    for dataset in datasets:
        for q in range(len(vquants)-1):
            lower = quantiles(surface_bright,vquants[q])
            upper = quantiles(surface_bright,vquants[q+1])
            all_sets.append(dataset[(surface_bright > lower) * (surface_bright < upper)])
    print len(all_sets)
    
    for mask in all_sets:
        print len(mask)
    for mask in datasets:
        print len(table[ (colors > hqvalue[0]) * (colors < hqvalue[len(hqvalue)-1])* (surface_bright > minsb) * (surface_bright < maxsb)]), 'good'
     
    # for i,mask in enumerate(all_sets):
    #     print i
    #     for gi,sb in zip(colors,surface_bright):
    #         if gi in table[mask]:
    #             if sb in table[mask]:
    #                 print i
    #         else:
    #             print -1
    
    plt.savefig('choose_quantiles.pdf')
    #os.system('cp choose_quantiles.pdf ~/public_html')
    #make_quantile_table(table, quantile_list)
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
    col8=pyf.Column(name='CG I-SB', format='1E',array=data['CG_I-SB'])
    col9=pyf.Column(name='QUANTILE',format='1E',array=quantile_list)
    col10=pyf.Column(name='CG_H50S',format='5E', array=data['CG_H50S'])
    col11=pyf.Column(name='CG_H90S', format='5E', array=data['CG_H90S'])
    cols=col1,col2,col3,col4,col5,col6,col7,col8,col9,col10, col11
    tbhdu=pyf.new_table(cols)
    tbhdulist=pyf.HDUList([hdu,tbhdu])
    tbhdulist.writeto('sdss_atlas_for_images_all.fits',clobber=True)

if __name__ == '__main__':    
    choose_quantiles(8, 4)
   
    
