# This file is part of the Sloan Atlas project.
# Copyright 2014 David W. Hogg (NYU).

import numpy as np
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

if __name__ == "__main__":
    fns = ["./test_data/A_0045-10_MCG_-2_3_16_irg.jpg",
           "./test_data/NGC_151_MCG_-2_2_54_IRAS_00315-0958_irg.jpg",
           "./test_data/NGC_173_UGC_369_IRAS_00346+0140_irg.jpg",
           "./test_data/NGC_7814_UGC_8_irg.jpg",
           ]
    make_one_plate([fns[ii] for ii in (1,2,3,0,1,2,3,3,3,0,1,2,3,0,1,2)], nx=2400).save("foo.jpg")
