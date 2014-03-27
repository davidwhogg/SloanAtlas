"""
This file is part of the Sloan Atlas project.
Copyright 2014 David W. Hogg (NYU) & Ekta Patel (NYU).

bugs:
-----
* Many things hard coded, brittle!
* Assumptions about directory structure.
"""

import os
import numpy as np
import pyfits as pf # works on broiler
from PIL import Image as im
import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text', usetex=True)
import matplotlib.pyplot as plt

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
        # check that the input image has even dimensions
        assert 2 * (thisim.size[0] / 2) == thisim.size[0]
        assert 2 * (thisim.size[1] / 2) == thisim.size[1]
        thisdata = np.asarray(thisim).copy()
        print thisdata.shape, np.min(thisdata), np.max(thisdata)
        # compute input and output pixel-offset locations
        x1 = iix * nxim
        y1 = iiy * nxim
        x2 = (thisim.size[0] - nxim) / 2
        y2 = (thisim.size[1] - nxim) / 2
        # now deal with possibility that input image is too small!
        thisnxim = nxim
        if x2 < 0 or y2 < 0:
            delta = np.max([-x2, -y2])
            x1 += delta
            y1 += delta
            x2 += delta
            y2 += delta
            thisnxim -= delta + delta
        print ii, iix, iiy, nxim, fn, thisim.size[0], x2, y2, thisnxim
        # attach white border to input data
        # note x <-> y issues
        thisdata[y2,:,:] = 255 # MAGIC 255
        thisdata[y2 + thisnxim - 1,:,:] = 255 # MAGIC 255
        thisdata[:,x2,:] = 255 # MAGIC 255
        thisdata[:,x2 + thisnxim - 1,:] = 255 # MAGIC 255
        # merge new data into plate canvas
        # note x <-> y issues
        platedata[y1:y1 + thisnxim,x1:x1 + thisnxim,:] = thisdata[y2:y2 + thisnxim,x2:x2 + thisnxim,:]
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

def make_one_caption_figure(names, fn, data):
    """
    bugs:
    * Needs more information in this comment header.
    * Wrong calling sequence given call (below)
    """
    print "make_one_caption_figure():", names, fn

    # massage data
    mags=data.field("CG_TOTMAGS")
    extinction=data.field("CG_EXTINCTION")
    
    mu50 = data.field("CG I-SB")
    fiducial = 3
    c = data.field("CG_H90S")[:,fiducial] / data.field("CG_H50S")[:,fiducial]
    u = mags[:,0]-extinction[:,0]
    g = mags[:,1]-extinction[:,1]
    r = mags[:,2]-extinction[:,2]
    i = mags[:,3]-extinction[:,3]
    z = mags[:,4]-extinction[:,4]

    plt.figure(figsize=(6,6))
    plt.subplots_adjust(hspace=0.08)

    ax = plt.subplot(211)
    ax.xaxis.set_visible(True)
    plt.setp(ax.get_xticklabels(),visible=False)
    gmi = g-i
    plt.plot(gmi, mu50, ".",
             color="0.6", alpha=0.5, mew=0, markeredgecolor="none")
    xlim = (0.2, 1.3)
    plt.xlim(xlim)
    plt.ylim(17.5, 24.1)
    plt.ylabel(r"$\mu_{50,i}~\mathrm{(mag)}$")
    def labelify(integer):
        return r"$\boldmath %s$" % ("%d" % integer).strip()
    for ii, name in enumerate(names):
        label = labelify(ii)
        jj = np.where(data["NAME"] == name)[0]
        print "make_one_caption_figure(): found objects with indices and quantiles:", jj, data[jj]["QUANTILE"]
        assert len(jj) == 1
        jj = jj[0]
        plt.plot(gmi[jj], mu50[jj], "+",
                 color="black", ms=5, markeredgecolor="black", clip_on=False)
        plt.text(gmi[jj], mu50[jj], label,
                 color="black", size="small", alpha=0.75, clip_on=False)
    
    plt.subplot(212)
    plt.plot(gmi, 1./c, ".",
             color="0.6", alpha=0.5, mew=0, markeredgecolor="none") # synchronized with above
    plt.xlim(xlim)
    plt.ylim(0.14, 0.36)
    plt.xlabel(r"$[g-i]~\mathrm{color~(mag)}$")
    plt.ylabel(r"$h_{50,i} / h_{90, i}$")
    for ii, name in enumerate(names):
        label = labelify(ii)
        jj = np.where(data["NAME"] == name)[0]
        print "make_one_caption_figure(): found objects with indices and quantiles:", jj, data[jj]["QUANTILE"]
        assert len(jj) == 1
        jj = jj[0]
        plt.plot(gmi[jj], 1./c[jj], "x",
                 color="black", ms=5, markeredgecolor="black", clip_on=False) # synchronized with above
        plt.text(gmi[jj], 1./c[jj], label,
                 color="black", size="small", alpha=0.75, clip_on=False) # synchronized with above
    plt.savefig(fn)
    return None

def make_one_quantile_of_plates(prefix, names, sizes, captions, tabdata):
    """
    inputs:
    - `prefix` - string for plate naming
    - `fns` - list of galaxy image file names
    - `sizes` - list of galaxy sizes in arcmin
    - `captions` - list of strings to put in captions for the plates

    outputs:
    - set of files `prefix`*.jpg
    - set of files `prefix`*.tex

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
    print captions
    nim = len(names)
    assert len(sizes) == nim
    assert len(captions) == nim
    platenum = 0
    while listindex < nim:
        thisprefix = "%s_%02d" % (prefix, platenum)
        outimgfn = "%s.jpg" % (thisprefix, )
        outtxtfn = "%s_caption.tex" % (thisprefix, )
        outfigfn = "%s_caption.png" % (thisprefix, )
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
            make_one_caption_figure(names[listindex:listindex + nimx * nimx], outfigfn, tabdata)
            fd = open(outtxtfn, "w")
            for ii in range(nimx * nimx):
                fd.write("%0d. --- %s\n" % (ii, captions[listindex + ii]))
                if ii < (nimx * nimx - 1):
                    fd.write("\\\\\n")
            fd.close()
        listindex += nimx * nimx
        platenum += 1
    return None

def remove_all_exceptions(data):
    """
    inputs:
    - `data` - structure with `NAME` tag

    outputs:
    - `data` with elements removed

    bugs:
    - Nothing but MAGIC.
    - Doesn't copy; changes in place; stupid.
    - All these exceptions need to be hand-inspected using flipbook files.
    """
    # remove bad data
    bad = np.zeros(len(data))
    # bad[np.where(data.NAME == "UGC 11891")] = 1 # looks red / wrong?
    bad[np.where(data.NAME == "A 1246-09")] = 1 # missing imaging data
    bad[np.where(data.NAME == "UGC 6773")] = 1 # bright star messing it up?
    bad[np.where(data.NAME == "NGC 3769A")] = 1 # bad deblend with B

    bad[np.where(data.NAME == "NGC 988")] = 1 # bright star messing it up?
    bad[np.where(data.NAME == "A 1646+62")] = 1 # bright star messing it up?
    bad[np.where(data.NAME == "UGC 6446")] = 1 # bright star messing it up?
    bad[np.where(data.NAME == "UGC 5245")] = 1 # missing data
    bad[np.where(data.NAME == "A 1420+45")] = 1 # missing data

    # bad[np.where(data.NAME == "NGC 2283")] = 1 # bad calibration or highly reddened?
    # bad[np.where(data.NAME == "UGC 11861")] = 1 # bad calibration or highly reddened?
    bad[np.where(data.NAME == "NGC 7741")] = 1 # missing imaging data
    # bad[np.where(data.NAME == "UGC 11818")] = 1 # bad calibration or highly reddened?
    bad[np.where(data.NAME == "NSA ID 131288")] = 1 # totally wrong and red and small
    # bad[np.where(data.NAME == "UGC 3433")] = 1 # bad calibration or highly reddened?

    bad[np.where(data.NAME == "A 2233-03")] = 1 # missing imaging data
    # bad[np.where(data.NAME == "UGC 2728")] = 1 # bad calibration or highly reddened?
    bad[np.where(data.NAME == "UGC 1230")] = 1 # missing imaging data
    bad[np.where(data.NAME == "UGC 6660")] = 1 # what the fuck?
    bad[np.where(data.NAME == "NGC 205")] = 1 # missing imaging data

    bad[np.where(data.NAME == "NGC 6070")] = 1 # missing imaging data
    bad[np.where(data.NAME == "NGC 7678")] = 1 # missing imaging data
    # bad[np.where(data.NAME == "UGC 2358")] = 1 # bad calibration or highly reddened?
    bad[np.where(data.NAME == "NGC 855")] = 1 # missing imaging data
    bad[np.where(data.NAME == "NGC 7497")] = 1 # missing imaging data
    bad[np.where(data.NAME == "NSA ID 133245")] = 1 # bright star messing it up?

    # bad[np.where(data.NAME == "UGC 2411")] = 1 # bad calibration or highly reddened?
    bad[np.where(data.NAME == "A 0102-06")] = 1 # missing imaging data
    bad[np.where(data.NAME == "UGC 2468")] = 1 # wrong size or galaxy cluster?
    bad[np.where(data.NAME == "NSA ID 44968")] = 1 # needs to be rerun in deblend mode

    bad[np.where(data.NAME == "UGC 2458")] = 1 # wrong size
    bad[np.where(data.NAME == "NGC 3640")] = 1 # missing imaging data
    bad[np.where(data.NAME == "NGC 7817")] = 1 # missing imaging data
    bad[np.where(data.NAME == "NGC 7771")] = 1 # missing imaging data
    bad[np.where(data.NAME == "NGC 4302")] = 1 # totally wrong JPEG; might just need rerunning

    bad[np.where(data.NAME == "NSA ID 33475")] = 1 # bright star messing it up?
    bad[np.where(data.NAME == "A 0106+01")] = 1 # bright star messing it up?
    bad[np.where(data.NAME == "UGC 10245")] = 1 # bad center / nothing there?
    bad[np.where(data.NAME == "NGC 7556")] = 1 # missing imaging data
    bad[np.where(data.NAME == "UGC 12206")] = 1 # missing imaging data

    # make (ill advised) adjustments
    data[np.where(data.NAME == "SEXTANS B")].CG_H50S[:,3] *= 2. # HACK wrong size?
    data[np.where(data.NAME == "SEXTANS B")].CG_H90S[:,3] *= 2. # HACK wrong size?
    print "removing %d galaxies:" % (np.sum(bad == 1),)
    print data.NAME[np.where(bad == 1)]
    data = data[bad == 0]
    return data

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
    tabdata = remove_all_exceptions(tabdata)
    fb = 3 # fiducial band MAGIC
    print 
    # the following is some made-up MAGIC 0.333 and MAGIC 24.0 and magic 2.5
    plotsizes = tabdata.CG_H50S[:,fb] * 10.**(0.333 * 0.4 * (24.0 - tabdata[:]["cg i-sb"]))
    plotsizes = np.clip(plotsizes, 2.5 * tabdata.CG_H50S[:,fb], np.Inf)
    assert len(plotsizes) == len(tabdata)
    captions = np.array(["~".join(nn.split(" ")) for nn in tabdata.NAME])
    assert len(captions) == len(tabdata)
    tiny = 1.e-3
    for quantile in range(np.round(np.max(tabdata.QUANTILE)).astype(int) + 1):
        prefix = "quantile_%02d" % quantile
        II = np.where(np.abs(tabdata.QUANTILE - quantile) < tiny)[0]
        II = II[(np.argsort(plotsizes[II]))[::-1]]
        print tabdata.NAME[II], tabdata.CG_H90S[II,fb], plotsizes[II]
        make_one_quantile_of_plates(prefix, tabdata.NAME[II], plotsizes[II], captions[II], tabdata)
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
