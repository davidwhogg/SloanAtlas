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
    - Written but not tested.
    '''
    nim = len(filelist)
    # get image grid size check that nim is a square
    nimx = np.round(np.sqrt(nim)).astype(int)
    assert nim == nimx * nimx
    # get individual-image sizes and check that the integers work
    nxim = nx / nimx # does this produce an int?
    assert nx == nimx * nxim
    # make plate canvas
    platedata = np.zeros((nx, nx, 3)).astype(int)
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
        thisdata = np.array(thisim.getdata()).reshape(thisim.size[0], thisim.size[1], 3) # MAGIC 3
        # compute input and output pixel-offset locations
        x1 = iix * nimx
        y1 = iiy * nimx
        x2 = (thisim.size[0] - nimx) / 2
        y2 = (thisim.size[1] - nimx) / 2
        print ii, iix, iiy, nxim, fn, thisim.size[0], x2
        # attach white border to input data
        thisdata[x2,:,:] = 255 # MAGIC 255
        thisdata[x2 + nimx - 1,:,:] = 255 # MAGIC 255
        thisdata[:,y2,:] = 255 # MAGIC 255
        thisdata[:,y2 + nimx - 1,:] = 255 # MAGIC 255
        # merge new data into plate canvas
        platedata[x1:x1 + nimx,y1:y1 + nimx,:] = thisdata[x2:x2 + nimx,y2:y2 + nimx,:]
    # make output image object
    plate = im.new("RGB", (nx, nx), "white")
    return plate

if __name__ == "__main__":
    print make_one_plate(["foo", "bar", "hello", "whatevs"])
