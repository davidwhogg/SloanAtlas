# This file is part of the Sloan Atlas project.
# Copyright 2012 David W. Hogg (NYU).

# Note that the curl is commented out.  Why?

FILEPREFIX = nsa_v0_1_2
SHORTENER = ./shorten_nsatlas.py
GZIP = gzip -fv --best

all: nsa-short.fits.gz

nsa-short.fits.gz: ${FILEPREFIX}.fits.gz ${SHORTENER}
	${SHORTENER} ${FILEPREFIX}.fits.gz nsa-short.fits
	${GZIP} nsa-short.fits

${FILEPREFIX}.fits.gz:
	curl -O http://sdss.physics.nyu.edu/mblanton/v0/${FILEPREFIX}.fits
	${GZIP} ${FILEPREFIX}.fits
