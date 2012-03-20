# This file is part of the Sloan Atlas project.
# Copyright 2012 David W. Hogg (NYU).

# Note that the curl is commented out.  Why?

FILEPREFIX = nsa_v0_1_2
SHORTENER = ./shorten_nsatlas.py

all: nsa-short.fits.gz

%.fits.gz: %.fits
	gzip --best $<

nsa-short.fits: ${FILEPREFIX}.fits.gz ${SHORTENER}
	${SHORTENER} ${FILEPREFIX}.fits.gz $@

#${FILEPREFIX}.fits:
#	curl -O http://sdss.physics.nyu.edu/mblanton/v0/$@

