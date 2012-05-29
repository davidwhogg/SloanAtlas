#creates 16 prospectus plots for the 16 largest galaxies (exemplars)

import matplotlib
import numpy as np
import pylab as plt
import pyfits as pyf
import os
import Image

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    a=data.field('RA')
    b=data.field('DEC')
    e=data.field('NSAID')
    f=data.field('DFLAGS')
    w=data.field('IAUNAME')
    y = data.field('SERSICFLUX')
    z = data.field('SERSIC_TH50')
    p50=data.field('PETROTH50')
    p90=data.field('PETROTH90')
    good=np.array([True for x in data.field('RA')])
    indx1=np.where(y[:,3] <= 0)
    good[indx1]=False
    indx2=np.where(y[:,1] <= 0)
    good[indx2]=False
    indx3=np.where(z > 158)
    good[indx3]=False


#creating compiled plots

fig1=plt.figure(1,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('88297.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar00_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 88297\nIAU Name: J121709.68+374453.6\nRA: 184.33094837\nDec: 37.778291532\nRadius: 152.228\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.474599 0.86972 0.947265 0.328399\nr magnitude: 12.5094\nComment:NONE')
plt.suptitle('color sample 0, i-sb sample 0',size=18)
plt.savefig('exemplar00.pdf')

fig2=plt.figure(2,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('158651.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar01_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 158651\nIAU Name: J104242.49+342650.9\nRA: 160.690485212\nDec: 34.4601866379\nRadius: 132.437\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.160236 0.756342 0.656239 0.232246\nr magnitude: 13.3138\nComment:NONE')
plt.suptitle('color sample 0, i-sb sample 1',size=18)
plt.savefig('exemplar01.pdf')

fig3=plt.figure(3,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('74038.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar02_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 74038\nIAU Name: J095004.51+124826.6\nRA: 147.51893804\nDec: 12.8074458979\nRadius: 150.584\nDflags: [64 64 64 64 64 64 64]\ncolors: 0.0743093 0.541951 0.350226 0.0920687\nr magnitude: 14.2201\nComment: Bad deblend, fleck of larger galaxy\nuser: blanton\ntime: 2011-10-23 12:05:24.328294-04:00')
plt.suptitle('color sample 0, i-sb sample 2',size=18)
plt.savefig('exemplar02.pdf')

fig4=plt.figure(4,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('143102.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar03_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 143102\nIAU Name: J131206.49+052832.9\nRA: 198.028901962\nDec: 5.47270152975\nRadius: 119.14\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.358387 0.875008 0.993238 0.503832\nr magnitude: 16.5479\nComment:NONE')
plt.suptitle('color sample 0, i-sb sample 3',size=18)
plt.savefig('exemplar03.pdf')

fig5=plt.figure(5,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('88298.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar10_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 88298\nIAU Name: J121729.43+374826.4\nRA: 184.372640795\nDec: 37.807344948\nRadius: 133.247\nDflags: [64 64  0  0  0  0  0]\ncolors: 0.73868 1.32216 1.2108 0.48205\nr magnitude: 11.9903\nComment:NONE')
plt.suptitle('color sample 1, i-sb sample 0',size=18)
plt.savefig('exemplar10.pdf')

fig6=plt.figure(6,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('158585.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar11_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 158585\nIAU Name: J103846.59+054145.0\nRA: 159.694884551\nDec: 5.69692579321\nRadius: 139.992\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.607283 1.33042 1.31338 0.659447\nr magnitude: 14.129\nComment:NONE')
plt.suptitle('color sample 1, i-sb sample 1',size=18)
plt.savefig('exemplar11.pdf')

fig7=plt.figure(7,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('31572.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar12_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 31572\nIAU Name: J135748.93+050528.1\nRA: 209.45391535\nDec: 5.09115329532\nRadius: 143.21\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.293571 1.1778 1.15792 0.60809\nr magnitude: 15.7264\nComment:NONE')
plt.suptitle('color sample 1, i-sb sample 2',size=18)
plt.savefig('exemplar12.pdf')

fig8=plt.figure(8,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('44000.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar13_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 44000\nIAU Name: J074815.83+284255.1\nRA: 117.06581331\nDec: 28.7154004455\nRadius: 151.014\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.411005 1.37549 0.881155 0.544497\nr magnitude: 15.8702\nComment:NONE')
plt.suptitle('color sample 1, i-sb sample 3',size=18)
plt.savefig('exemplar13.pdf')

fig9=plt.figure(9,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('166141.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar20_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 166141\nIAU Name: J152156.39+050410.9\nRA: 230.485358419\nDec: 5.07063311934\nRadius: 150.819\nDflags: [64 64 64  0  0  0  0]\ncolors: 0.778852 1.92399 1.63868 0.745632\nr magnitude: 12.3383\nComment:NONE')
plt.suptitle('color sample 2, i-sb sample 0',size=18)
plt.savefig('exemplar20.pdf')

fig10=plt.figure(10,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('126043.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar21_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 126043\nIAU Name: J000138.30+232901.0\nRA: 0.409697110691\nDec: 23.4836206985\nRadius: 118.375\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.840847 2.17525 1.74247 1.08662\nr magnitude: 14.2478\nComment:NONE')
plt.suptitle('color sample 2, i-sb sample 1',size=18)
plt.savefig('exemplar21.pdf')

fig11=plt.figure(11,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('54244.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar22_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 54244\nIAU Name: J162523.24+375547.9\nRA: 246.346882326\nDec: 37.9299951474\nRadius: 131.732\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.404303 1.58834 1.46829 0.670803\nr magnitude: 15.0726\nComment:NONE')
plt.suptitle('color sample 2, i-sb sample 2',size=18)
plt.savefig('exemplar22.pdf')

fig12=plt.figure(12,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('5029.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar23_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 5029\nIAU Name: J220632.50-002052.4\nRA: 331.635441909\nDec: -0.347901617088\nRadius: 132.733\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.793285 2.25606 0.897457 0.601278\nr magnitude: 15.1693\nComment:NONE')
plt.suptitle('color sample 2, i-sb sample 3',size=18)
plt.savefig('exemplar23.pdf')

fig13=plt.figure(13,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('83634.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar30_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 83634\nIAU Name: J095620.36+694200.5\nRA: 148.971219347\nDec: 69.6800566999\nRadius: 137.82\nDflags: [0 0 0 0 0 0 0]\ncolors: 1.47196 2.56263 1.88025 0.748447\nr magnitude: 10.4695\nComment:NONE')
plt.suptitle('color sample 3, i-sb sample 0',size=18)
plt.savefig('exemplar30.pdf')

fig14=plt.figure(14,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('162413.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar31_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 162413\nIAU Name: J124718.76-024258.6\nRA: 191.826387119\nDec: -2.71785936216\nRadius: 144.547\nDflags: [88 80 64  0  0  0 64]\ncolors: 8.70745 5.32085 1.43866 0.567597\nr magnitude: 12.4078\nComment:NONE\n* u-g & g-r colors very high and therefore out of range of plot')
plt.suptitle('color sample 3, i-sb sample 1',size=18)
plt.savefig('exemplar31.pdf')

fig15=plt.figure(15,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('155176.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar32_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 155176\nIAU Name: J024240.70+000047.0\nRA: 40.6869070175\nDec: 0.0156059515691\nRadius: 129.961\nDflags: [80 80  0  0 64  0 64]\ncolors: 2.46681 3.65421 0.886092 0.5443\nr magnitude: 13.0715\nComment:NONE\n*u-g is out of range of plot')
plt.suptitle('color sample 3, i-sb sample 2',size=18)
plt.savefig('exemplar32.pdf')

fig16=plt.figure(16,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('139151.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('exemplar33_plot3.png')
plt.imshow(im,origin='lower')

#text, get from exemplars.log
plt.figtext(0.15 ,.05, u'NSAID: 139151\nIAU Name: J111905.10+580121.9\nRA: 169.771205657\nDec: 58.0228197395\nRadius: 115.11\nDflags: [24  0  0  0  0  0  0]\ncolors: 2.03708 3.02141 1.18692 0.579468\nr magnitude: 16.356\nComment:NONE')
plt.suptitle('color sample 3, i-sb sample 3',size=18)
plt.savefig('exemplar33.pdf')


plt.show()