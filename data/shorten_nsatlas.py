#!/usr/bin/env python
'''
This file is part of the Sloan Atlas project.
Copyright 2012 David W. Hogg (NYU).

All this code does is shorten the NASA-Sloan Atlas input file.
'''
import sys
import pyfits as pyf
import numpy as np

if __name__ == '__main__':
    # read FITS table
    print "%s: reading %s ..." % (sys.argv[0], sys.argv[1])
    hdulist = pyf.open(sys.argv[1])
    data = hdulist[1].data
    hdulist.close()
    # put filtering here to shorten data
    print "%s: filtering content ..." % sys.argv[0]
    big = (data.field('SERSIC_TH50') > 30.) # arcsec
    print "%s: data before: %d" % (sys.argv[0], len(data))
    data = data[big]
    print "%s: data after: %d" % (sys.argv[0], len(data))
    # now create new FITS table
    print "%s: writing %s ..." % (sys.argv[0], sys.argv[2])
    hdu = pyf.PrimaryHDU()
    tbhdu = pyf.new_table(hdulist[1].columns)
    tbhdu.data = data
    tbdulist = pyf.HDUList([hdu, tbhdu])
    tbdulist.writeto(sys.argv[2])
    print "%s: ... done" % sys.argv[0]
