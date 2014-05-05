from astrometry.util.starutil import *

def iau_name(ra,dec):
    (rh, rm ,rs) = ra2hms(ra)
    (sgn, dd ,dm, ds) = dec2dms(dec)

    rcs = int(rs *100.)
    dds = int(ds * 10.)

    return 'J%02i%02i%02i.%02i%s%02i%02i%02i.%01i' % (
            rh, rm, rcs / 100, rcs % 100,
            '+' if sgn >= 0 else '-',
            dd, dm, dds / 10, dds % 10)

# print iau_name(15,1)
# print iau_name(0,0)
# print iau_name(0, 1./3600)
# print iau_name(0,1./36000)
# print iau_name(0,1./36001)
# print iau_name(15/60.,1)
# print iau_name(15/3600.,1)
# print iau_name(15/360000,1)
# print iau_name(15/360001,1)
# print iau_name(375.,-0.5)
# print iau_name(375.,0.5)
# print iau_name(360.,90.)
