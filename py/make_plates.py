# This file is part of the Sloan Atlas project.
# Copyright 2014 David W. Hogg (NYU).

import os
import numpy as np
import pyfits as pf # works on broiler
from PIL import Image as im

FIDUCIAL = 5. * 60. # MAGIC number in arcsec

def make_one_plate(filelist, nx=2424):
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
        print "opening %s" % (fn, )
        thisim = im.open(fn)
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
        print ii, iix, iiy, nxim, fn, thisim.size[0], x2, y2
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

def move_files_from_remote_server(names):
    """
    inputs:
    - `names` - galaxy names (possibly including wild cards)

    returns:
    - `fns` - file names of local files, or null string when failures occur.

    bugs:
    - Way too much hard-coded.
    """
    rfns = np.array(["_".join(nn.split(" ")) + "_*irg_clean.jpg" for nn in names])
    fns = np.array([])
    for rfn in rfns:
    # need to check for existence of fn or else scp it from bootes
        print "looking for %s" % (rfn, )
        fn = os.popen("ls " + rfn).read().rstrip()
        if not os.path.exists(fn):
            cmd = "scp bootes:/global/data/scr/dwh3/ep109/all_images/" + rfn + " ."
            print cmd
            os.system(cmd)
            fn = os.popen("ls " + rfn).read().rstrip()
        if not os.path.exists(fn):
            print "didn't ever get %s; setting False" % (rfn, )
            fn = ""
        fns = np.append(fns, fn)
    return fns

def make_one_quantile_of_plates(prefix, names, sizes, captions):
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
    - MAGIC number(s).
    - Only skeleton code; doesn't actually work.
    """
    listindex = 0
    nim = len(names)
    assert len(sizes) == nim
    assert len(captions) == nim
    # bring in files and trim to the "successful" list
    fns = move_files_from_remote_server(names)
    II = (fns != "")
    names = names[II]
    sizes = sizes[II]
    captions = captions[II]
    fns = fns[II]
    captions = [cc + " " + ff for (cc, ff) in zip(captions, fns)]
    print captions
    nim = len(names)
    assert len(sizes) == nim
    assert len(captions) == nim
    platenum = 0
    while listindex < nim:
        thisprefix = "%s_%02d" % (prefix, platenum)
        outimgfn = "%s.jpg" % (thisprefix, )
        outtxtfn = "%s.txt" % (thisprefix, )
        nimx = int(np.floor(FIDUCIAL / sizes[listindex]))
        if nimx < 1: nimx = 1
        if nimx > 4: nimx = 4
        if listindex + nimx * nimx > nim:
            break
        if os.path.exists(outimgfn):
            print "already made %s" % (outimgfn, )
        else:
            print "making %s" % (outimgfn, )
            make_one_plate(fns[listindex:listindex + nimx * nimx]).save(outimgfn)
            fd = open(outtxtfn, "w") # wrong syntax?
            for ii in range(nimx * nimx):
                fd.write("%0d --- %0d --- %s\n" % (platenum, ii, captions[listindex + ii]))
            fd.close()
        listindex += nimx * nimx
        platenum += 1
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
    - Assumes quantile values are reals!
    """
    tabdata = pf.open(catalogfn)[1].data
    fb = 3 # fiducial band MAGIC
    tabdata = tabdata[(np.argsort(tabdata.CG_H90S[:,fb]))[::-1]]
    print tabdata.shape
    tiny = 1.e-3
    for quantile in range(np.round(np.max(tabdata.QUANTILE)).astype(int) + 1):
        prefix = "quantile_%02d" % quantile
        II = (np.abs(tabdata.QUANTILE - quantile) < tiny)
        print tabdata.NAME[II]
        print tabdata.CG_H90S[II,fb]
        make_one_quantile_of_plates(prefix, tabdata.NAME[II], tabdata.CG_H90S[II, fb], tabdata.NAME[II])
    return None

if __name__ == "__main__":
    make_all_plates("/data1/ep1091/tractor/sdss_atlas_plates_quants.fits")

if False:
    fns = ["./test_data/A_0045-10_MCG_-2_3_16_irg.jpg",
           "./test_data/NGC_151_MCG_-2_2_54_IRAS_00315-0958_irg.jpg",
           "./test_data/NGC_173_UGC_369_IRAS_00346+0140_irg.jpg",
           "./test_data/NGC_7814_UGC_8_irg.jpg",
           ]
    make_one_plate([fns[ii] for ii in (1,2,3,0,1,2,3,3,3,0,1,2,3,0,1,2)], nx=2424).save("foo.jpg")

