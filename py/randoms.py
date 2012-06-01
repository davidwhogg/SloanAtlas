#creates 16 prospectus plots for the 16 largest galaxies (random)

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
im=Image.open('142962.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random00_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 142962\nIAU Name: J130549.49+373618.0\nRA: 196.456881064\nDec: 37.6105458272\nRadius: 88.3863\nDflags: [64 64  0  0  0  0  0]\ncolors: 0.243078 0.562761 0.930488 0.227574\nr magnitude: 13.0584\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 0, i-sb sample 0',size=18)
plt.savefig('random00.pdf')

fig2=plt.figure(2,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('138272.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random01_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 138272\nIAU Name: J105300.09+173424.9\nRA: 163.250820384\nDec: 17.5735599745\nRadius: 39.2846\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.354592 1.0544 0.940308 0.42396\nr magnitude: 14.6945\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 0, i-sb sample 1',size=18)
plt.savefig('random01.pdf')

fig3=plt.figure(3,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('69210.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random02_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'604\nNSAID: 69210\nIAU Name: J145938.25+444022.7\nRA: 224.909371831\nDec: 44.673005825\nRadius: 36.9291\nDflags: [0 0 0 0 0 0 0]\ncolors: -0.0599766 0.455718 0.467999 0.235034\nr magnitude: 15.2483\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 0, i-sb sample 2',size=18)
plt.savefig('random02.pdf')

fig4=plt.figure(4,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('28067.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random03_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 28067\nIAU Name: J134417.11+611406.2\nRA: 206.071410697\nDec: 61.2352001738\nRadius: 44.3851\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.0160046 1.03231 0.767139 0.552578\nr magnitude: 16.8294\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 0, i-sb sample 3',size=18)
plt.savefig('random03.pdf')

fig5=plt.figure(5,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('154089.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random10_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 154089\nIAU Name: J011944.49+032435.0\nRA: 19.9371139562\nDec: 3.40984215725\nRadius: 30.9563\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.662194 1.61925 1.27763 0.757816\nr magnitude: 13.6599\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 1, i-sb sample 0',size=18)
plt.savefig('random10.pdf')

fig6=plt.figure(6,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('142446.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random11_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 142446\nIAU Name: J125145.90+254636.9\nRA: 192.93982841\nDec: 25.7744694375\nRadius: 59.577\nDflags: [64 64  0 64 64 64  0]\ncolors: 0.321854 1.25311 1.13364 0.541368\nr magnitude: 13.7074\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 1, i-sb sample 1',size=18)
plt.savefig('random11.pdf')

fig7=plt.figure(7,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('146349.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random12_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 146349\nIAU Name: J154219.39+002828.0\nRA: 235.581439431\nDec: 0.473681027364\nRadius: 41.562\nDflags: [0 0 0 0 0 0 0]\ncolors: 0.268042 1.52936 0.860393 0.394058\nr magnitude: 15.8765\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 1, i-sb sample 2',size=18)
plt.savefig('random12.pdf')

fig8=plt.figure(8,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('140045.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random13_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 140045\nIAU Name: J114046.69+210227.0\nRA: 175.197650889\nDec: 21.0505077667\nRadius: 137.102\nDflags: [64 64  0  0  0  0  0]\ncolors: 0.709116 1.68026 1.02429 0.452716\nr magnitude: 15.9128\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 1, i-sb sample 3',size=18)
plt.savefig('random13.pdf')

fig9=plt.figure(9,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('149192.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random20_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 149192\nIAU Name: J213001.89+264303.9\nRA: 322.508019217\nDec: 26.7178676731\nRadius: 50.5473\nDflags: [64 64  0  0  0  0  0]\ncolors: 1.24305 2.0425 1.51059 0.86763\nr magnitude: 14.1373\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 2, i-sb sample 0',size=18)
plt.savefig('random20.pdf')

fig10=plt.figure(10,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('145871.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random21_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 145871\nIAU Name: J150924.70-104144.0\nRA: 227.3530972\nDec: -10.6952443174\nRadius: 53.2297\nDflags: [64  0  0  0  0  0  0]\ncolors: 0.348892 2.05642 1.93668 0.963023\nr magnitude: 15.2737\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 2, i-sb sample 1',size=18)
plt.savefig('random21.pdf')

fig11=plt.figure(11,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('157310.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random22_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 157310\nIAU Name: J093258.39+273001.0\nRA: 143.244557495\nDec: 27.5000796798\nRadius: 43.9751\nDflags: [64 64  0 64  0  0  0]\ncolors: 0.629978 1.54468 1.75965 0.867525\nr magnitude: 15.8224\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 2, i-sb sample 2',size=18)
plt.savefig('random22.pdf')

fig12=plt.figure(12,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('96631.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random23_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 96631\nIAU Name: J150234.67+245408.5\nRA: 225.64459878\nDec: 24.9022947069\nRadius: 79.7999\nDflags: [ 0 16  0  0  0  0  0]\ncolors: -0.210245 2.64612 0.749023 0.873557\nr magnitude: 17.0371\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 2, i-sb sample 3',size=18)
plt.savefig('random23.pdf')

fig13=plt.figure(13,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('162027.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random30_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 162027\nIAU Name: J123402.89+074201.0\nRA: 188.512465128\nDec: 7.6993165801\nRadius: 35.9019\nDflags: [64 64  0  0  0  0  0]\ncolors: 1.42511 2.90308 1.86532 0.842949\nr magnitude: 12.2425\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 3, i-sb sample 0',size=18)
plt.savefig('random30.pdf')

fig14=plt.figure(14,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('140952.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random31_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 140952\nIAU Name: J121348.29+145400.9\nRA: 183.45120225\nDec: 14.900455937\nRadius: 75.1687\nDflags: [ 3 64 64 64 64 64 64]\ncolors: inf 4.64978 2.16479 1.1742\nr magnitude: 13.9672\nComment:NONE\n*all 4 colors are out of range here')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 3, i-sb sample 1',size=18)
plt.savefig('random31.pdf')

fig15=plt.figure(15,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('140377.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random32_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 140377\nIAU Name: J115240.90+200856.9\nRA: 178.172597135\nDec: 20.1476017314\nRadius: 36.2855\nDflags: [64  0  0  0  0  0  0]\ncolors: 1.22829 3.36968 1.83345 0.901284\nr magnitude: 15.8347\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 3, i-sb sample 2',size=18)
plt.savefig('random32.pdf')

fig16=plt.figure(16,figsize=(9,8))
plt.subplots_adjust(top=0.9,hspace=0.1,bottom=0.3)
#galaxy
plt.subplot(121)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('155051.jpg')
plt.imshow(im,origin='lower')

#plots with star
plt.subplot(122)
plt.tick_params(axis='both',labelbottom='off',labelleft='off',length=0)
im=Image.open('random33_plot.png')
plt.imshow(im,origin='lower')

#text, get from randoms.log
plt.figtext(0.15 ,.05, u'NSAID: 155051\nIAU Name: J022642.10+244757.0\nRA: 36.6756392134\nDec: 24.7995418005\nRadius: 35.8436\nDflags: [64  0  0  0  0  0  0]\ncolors: 0.432373 3.4349 1.98408 1.0056\nr magnitude: 16.5346\nComment:NONE')
plt.figtext(0.9,0.9,'random',color='gray')
plt.suptitle('color sample 3, i-sb sample 3',size=18)
plt.savefig('random33.pdf')

plt.show()