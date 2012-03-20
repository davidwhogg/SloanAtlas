FILEPREFIX = nsa_v0_1_2

all: ${FILEPREFIX}.fits.gz

${FILEPREFIX}.fits.gz: $${FILEPREFIX}.fits
	gzip --best ${FILEPREFIX}.fits

${FILEPREFIX}.fits:
	curl -O http://sdss.physics.nyu.edu/mblanton/v0/${FILEPREFIX}.fits
