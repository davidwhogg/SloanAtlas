# This file is part of the Sloan Atlas project.
# Copyright 2014 David W. Hogg (NYU).

import os
import numpy as np
import pyfits as pf # works on broiler
from PIL import Image as im

def make_one_plate(filelist, nx=2400):
    '''
    inputs:
    - `filelist` -- list of image files
    - `nx` (optional) -- plate outer edge side

    output:
    - `PIL` image object

    bugs:
    - Very brittle; assumes input is `PIL RGB` format.
    - Can only make square plates with square subimages.
    '''
    nim = len(filelist)
    # get image grid size check that nim is a square
    nimx = np.round(np.sqrt(nim)).astype(int)
    assert nim == nimx * nimx
    # get individual-image sizes and check that the integers work
    nxim = nx / nimx # does this produce an int?
    assert nx == nimx * nxim
    # make plate canvas
    platedata = np.zeros((nx, nx, 3)).astype(np.uint8)
    # loop over file names
    for ii, fn in enumerate(filelist):
        iix = ii % nimx
        iiy = ii / nimx
        # need to check for existence of fn or else scp it from bootes
        rfn = os.popen("ls " + fn).read()
        if not os.path.exists(rfn):
            cmd = "scp bootes:/global/data/scr/dwh3/ep109/all_images/" + fn + " ."
            print cmd
            os.system(cmd)
            rfn = os.popen("ls " + fn).read().rstrip()
        thisim = im.open(rfn)
        # check that the input image is large enough and has even dimensions
        assert thisim.size[0] >= nxim
        assert thisim.size[1] >= nxim
        assert 2 * (thisim.size[0] / 2) == thisim.size[0]
        assert 2 * (thisim.size[1] / 2) == thisim.size[1]
        thisdata = np.asarray(thisim).copy()
        print thisdata.shape, np.min(thisdata), np.max(thisdata)
        # compute input and output pixel-offset locations
        x1 = iix * nxim
        y1 = iiy * nxim
        x2 = (thisim.size[0] - nxim) / 2
        y2 = (thisim.size[1] - nxim) / 2
        print ii, iix, iiy, nxim, rfn, thisim.size[0], x2, y2
        # attach white border to input data
        # note x <-> y issues
        thisdata[y2,:,:] = 255 # MAGIC 255
        thisdata[y2 + nxim - 1,:,:] = 255 # MAGIC 255
        thisdata[:,x2,:] = 255 # MAGIC 255
        thisdata[:,x2 + nxim - 1,:] = 255 # MAGIC 255
        # merge new data into plate canvas
        # note x <-> y issues
        platedata[y1:y1 + nxim,x1:x1 + nxim,:] = thisdata[y2:y2 + nxim,x2:x2 + nxim,:]
    # make output image object
    print platedata.shape, np.min(platedata), np.max(platedata)
    plate = im.fromarray(platedata)
    return plate

def make_one_quantile_of_plates(prefix, fns, sizes, captions):
    """
    inputs:
    - `prefix` - string for plate naming
    - `fns` - list of galaxy image file names
    - `sizes` - list of galaxy sizes in arcmin
    - `captions` - list of strings to put in captions for the plates

    outputs:
    - set of files `prefix`*.jpg
    - set of files `prefix`*.txt

    bugs:
    - Only skeleton code; doesn't actually work.
    """
    listindex = 0
    nim = len(fns)
    assert len(sizes) == nim
    while listindex < nim:
        fiducial = 6. * 60. # MAGIC number in arcsec
        print fiducial, listindex, sizes[listindex]
        nimx = int(np.floor(fiducial / sizes[listindex]))
        if nimx < 1: nimx = 1
        if nimx > 4: nimx = 4
        if listindex + nimx * nimx > nim:
            break
        thisprefix = "%s_%03d" % (prefix, listindex)
        outimgfn = "%s.jpg" % (thisprefix, )
        outtxtfn = "%s.txt" % (thisprefix, )
        make_one_plate(fns[listindex:listindex + nimx * nimx]).save(outimgfn)
        fd = open(outtxtfn, "w") # wrong syntax?
        for ii in range(nimx * nimx):
            print fd, ii, captions[listindex + ii] # wrong syntax
        fd.close()
        listindex += nimx * nimx
    return None

def make_all_plates(catalogfn):
    """
    inputs:
    - `catalogfn` - fits file name with SloanAtlas data table

    outputs:
    - plate images

    bugs:
    - Not even close to working.
    - Assumes no quantile is < 0.
    """
    tabdata = pf.open(catalogfn)[1].data
    fb = 3 # fiducial band MAGIC
    tabdata = tabdata[(np.argsort(tabdata.CG_H90S[:,fb]))[::-1]]
    filenames = np.array(["_".join(q.split(" ")) + "_*irg.jpg" for q in tabdata.NAME])
    for quantile in range(np.max(tabdata.QUANTILE)):
        prefix = "quantile_%02d" % quantile
        II = (tabdata.QUANTILE == quantile)
        print filenames[II]
        print tabdata[II].CG_H90S[:,fb]
        make_one_quantile_of_plates(prefix, filenames[II], tabdata.CG_H90S[II, fb], tabdata[II].NAME)
    return None

if __name__ == "__main__":
    make_all_plates("/data1/ep1091/tractor/sdss_atlas_for_images_all.fits")
    
if False:
    fns = ["./test_data/A_0045-10_MCG_-2_3_16_irg.jpg",
           "./test_data/NGC_151_MCG_-2_2_54_IRAS_00315-0958_irg.jpg",
           "./test_data/NGC_173_UGC_369_IRAS_00346+0140_irg.jpg",
           "./test_data/NGC_7814_UGC_8_irg.jpg",
           ]
    make_one_plate([fns[ii] for ii in (1,2,3,0,1,2,3,3,3,0,1,2,3,0,1,2)], nx=2400).save("foo.jpg")

