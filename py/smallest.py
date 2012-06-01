#creates 16 prospectus plots for the 16 largest galaxies (smallest)

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
im=Image.open('141654.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest00_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 141654\nIAU Name: J123419.29+062804.0\nRA: 188.578914315\nDec: 6.47062072906\nRadius: 30.3453\nDflags: [ 0  0  0  0  0 64  0]\ncolors: 0.421813 0.662337 0.647705 0.30473\nr magnitude: 12.7735\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 0, i-sb sample 0',size=18)
plt.savefig('smallest00.pdf')

fig2=plt.figure(2,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('162575.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest01_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 162575\nIAU Name: J125450.90+023912.0\nRA: 193.71282252\nDec: 2.65413454923\nRadius: 30.2844\nDflags: [64 64  0  0  0  0  0]\ncolors: 0.176173 0.487822 0.631904 0.235359\nr magnitude: 14.5791\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 0, i-sb sample 1',size=18)
plt.savefig('smallest01.pdf')

fig3=plt.figure(3,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('165451.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest02_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 165451\nIAU Name: J144302.00+044605.0\nRA: 220.764682973\nDec: 4.7637570804\nRadius: 30.0383\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.426428 0.787231 1.11589 0.449593\nr magnitude: 16.331\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 0, i-sb sample 2',size=18)
plt.savefig('smallest02.pdf')

fig4=plt.figure(4,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('44545.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest03_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 44545\nIAU Name: J011838.07-001531.9\nRA: 19.658644739\nDec: -0.258881907333\nRadius: 30.2752\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.191883 0.626129 0.865206 0.282061\nr magnitude: 18.0878\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 0, i-sb sample 3',size=18)
plt.savefig('smallest03.pdf')

fig5=plt.figure(5,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('137237.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest10_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 137237\nIAU Name: J102356.49-031056.0\nRA: 155.98537998\nDec: -3.18210681756\nRadius: 30.0261\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.733416 1.42149 1.50455 0.733896\nr magnitude: 14.7369\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 1, i-sb sample 0',size=18)
plt.savefig('smallest10.pdf')

fig6=plt.figure(6,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('129827.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest11_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 129827\nIAU Name: J013007.50+255150.0\nRA: 22.5316691297\nDec: 25.8623986078\nRadius: 30.0426\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.343962 1.36954 1.09159 0.504098\nr magnitude: 15.5771\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 1, i-sb sample 1',size=18)
plt.savefig('smallest11.pdf')

fig7=plt.figure(7,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('8756.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest12_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 8756\nIAU Name: J013317.71+131956.0\nRA: 23.3237672701\nDec: 13.3320293394\nRadius: 30.2575\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.397789 1.3343 1.16988 0.553428\nr magnitude: 15.8393\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 1, i-sb sample 2',size=18)
plt.savefig('smallest12.pdf')

fig8=plt.figure(8,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('115565.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest13_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 115565\nIAU Name: J162601.59+095149.7\nRA: 246.506645763\nDec: 9.8638163259\nRadius: 30.4436\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.82634 1.86699 0.790836 0.397505\nr magnitude: 17.5835\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 1, i-sb sample 3',size=18)
plt.savefig('smallest13.pdf')

fig9=plt.figure(9,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('93093.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest20_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 93093\nIAU Name: J121007.96+355239.3\nRA: 182.533169073\nDec: 35.8776119177\nRadius: 30.0485\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.725645 2.13557 1.79382 0.863785\nr magnitude: 15.0763\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 2, i-sb sample 0',size=18)
plt.savefig('smallest20.pdf')

fig10=plt.figure(10,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('76778.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest21_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 76778\nIAU Name: J090958.07+621450.7\nRA: 137.49191917\nDec: 62.2474599357\nRadius: 30.0243\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.873741 1.97665 1.55458 0.870994\nr magnitude: 14.9569\nComment: Strong dust lane\nuser: blanton\ntime: 2011-07-14 13:27:00.894965-04:00')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 2, i-sb sample 1',size=18)
plt.savefig('smallest21.pdf')

fig11=plt.figure(11,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('133790.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest22_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 133790\nIAU Name: J042653.29-035255.0\nRA: 66.7220826149\nDec: -3.88186616411\nRadius: 30.04\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.758352 1.42962 1.60784 0.792792\nr magnitude: 16.2915\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 2, i-sb sample 2',size=18)
plt.savefig('smallest22.pdf')

fig12=plt.figure(12,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('66672.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest23_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 66672\nIAU Name: J122513.11+130131.4\nRA: 186.304673771\nDec: 13.0254223502\nRadius: 30.016\nDflags: [16  0  0  0  0  0  0]\ncolors: 3.72764 2.67791 1.27962 0.579672\nr magnitude: 18.0612\nComment: Nucleated dE, probably at Virgo\nuser: blanton\ntime: 2011-07-25 23:59:39.751393-04:00\n*u-g color out of range of plot')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 2, i-sb sample 3',size=18)
plt.savefig('smallest23.pdf')

fig13=plt.figure(13,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('141473.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest30_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 141473\nIAU Name: J122859.99+135842.9\nRA: 187.250165331\nDec: 13.9785351235\nRadius: 30.0199\nDflags: [66 66  0  0  0  0  0]\ncolors: -0.534691 17.933 1.86417 0.878675\nr magnitude: 12.6767\nComment:NONE\n*g-r out of range')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 3, i-sb sample 0',size=18)
plt.savefig('smallest30.pdf')

fig14=plt.figure(14,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('91658.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest31_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 91658\nIAU Name: J105007.28+362030.5\nRA: 162.530347145\nDec: 36.3418594293\nRadius: 30.1298\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.925955 3.1418 1.85229 0.835196\nr magnitude: 15.1805\nComment: S0 or spiral, inner bar and ring, small close companion\nuser: blanton\ntime: 2011-08-13 18:40:34.774415-04:00')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 3, i-sb sample 1',size=18)
plt.savefig('smallest31.pdf')

fig15=plt.figure(15,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('136051.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest32_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 136051\nIAU Name: J094333.09+392453.9\nRA: 145.887873963\nDec: 39.4151003656\nRadius: 30.0516\nDflags: [64 64  0  0  0  0  0]\ncolors: 0.944538 3.15012 1.88177 0.911551\nr magnitude: 15.653\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 3, i-sb sample 2',size=18)
plt.savefig('smallest32.pdf')

fig16=plt.figure(16,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('98900.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('smallest33_plot.png')
plt.imshow(im,origin='lower')

#text, get from smallests.log
plt.figtext(0.15 ,.05, u'NSAID: 98900\nIAU Name: J160151.95+154732.1\nRA: 240.466484518\nDec: 15.792252431\nRadius: 30.2827\nDflags: [0 0 0 0 0 0 0]\ncolors: 1.1889 3.32635 1.69635 0.757287\nr magnitude: 16.5095\nComment:NONE')
plt.figtext(0.9,0.9,'smallest',color='gray')
plt.suptitle('color sample 3, i-sb sample 3',size=18)
plt.savefig('smallest33.pdf')

plt.show()