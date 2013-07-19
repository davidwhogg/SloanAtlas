import inspect
import sys
import os
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text', usetex=True)

import matplotlib.pyplot as plt
import pyfits as pyf

def color_prop(fits,fn1, objects=[],labels=[]):
    table=pyf.open('%s.fits'%(fits))
    data=table[1].data
    mags=data.field('CG_TOTMAGS')
    extinction=data.field('CG_EXTINCTION')
    c=data.field('CG_CONC')
    c=c[:,3]
    mu50=data.field('CG_I-SB')
    u=mags[:,0]-extinction[:,0]
    g=mags[:,1]-extinction[:,1]
    r=mags[:,2]-extinction[:,2]
    i=mags[:,3]-extinction[:,3]
    z=mags[:,4]-extinction[:,4]

 #fig, axes = subplot(2,1, sharex=True)   
    plt.figure(figsize=(6,6))
    plt.subplots_adjust(hspace=0.08)
    ax=plt.subplot(211)
    ax.xaxis.set_visible(True)
    plt.setp(ax.get_xticklabels(),visible=False)

    x=g-i
    plt.plot(x, mu50, 'o',color="0.6",mew=0, alpha=0.5, markeredgecolor='none')
    plt.xlim(0.1,1.4)
    plt.ylim(16,26)
    
    plt.ylabel(r'$\mu_{50,i}$')
    for j in range(0,len(objects)):
        x=g[j]-i[j]
        plt.plot(x, mu50[j], 'o', color='black',ms=5, markeredgecolor='black')
        plt.annotate(labels[j], xy=(x,mu50[j]), xytext=(x,mu50[j]+0.15),xycoords='data',textcoords='data',color='black',size='large')
    

    plt.subplot(212)
    x=g-i
    plt.plot(x, c, 'o',color="0.6", alpha=0.5, mew=0, markeredgecolor='none')
    plt.xlim(0.1,1.4)
    plt.ylim(2,5)
    plt.xlabel(r'$g-i$')
    plt.ylabel(r'$C_i$')
    for j in range(0,len(objects)):
        x=g[j]-i[j]
        plt.plot(x, c[j], 'o', color='black',ms=5, markeredgecolor='black')
        plt.annotate(labels[j], xy=(x,c[j]), xytext=(x,c[j]+0.15),xycoords='data',textcoords='data',color='black',size='large')
    plt.savefig('%s.pdf' %(fn1))
 
color_prop('sdss_atlas_2013','tester', objects=[1,2,3,4,5], labels=['A','B','C','D','E'])

