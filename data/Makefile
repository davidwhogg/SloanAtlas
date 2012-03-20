FILEPREFIX = nsa_v0_1_2
SHORTENER = ./shorten_nsatlas.py

all: nsa-short.fits.gz

%.fits.gz: %.fits
	gzip --best $<

${FILEPREFIX}.fits:
	curl -O http://sdss.physics.nyu.edu/mblanton/v0/$@

nsa-short.fits: ${FILEPREFIX}.fits.gz ${SHORTENER}
	${SHORTENER} ${FILEPREFIX}.fits.gz $@
