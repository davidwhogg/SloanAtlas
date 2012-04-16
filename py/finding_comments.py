import matplotlib
import numpy as np
import pylab as plt
import pyfits as pyf
import yanny as yanny

if __name__ == '__main__':
    data = pyf.open("../data/nsa-short.fits.gz")[1].data
    y=data.field('NSAID')
    x=data.field('SERSICFLUX')
    z=yanny.yanny(filename='comments.par')
    print type(z)
    def bad(x):
        for t in x:
           if t < 0 : print t
           if t < 0 : d=y[t] #gives NSAID 
           if t < 0 : print d
           if t < 0 : print yanny.row(z,1,d) # this is not the right function to do this but I want 
           #it to find the row in the comments file that includes the galaxy with a bad flux 
           #(by its NSAID), its probably more complicated than this
        return x 
    
    c=bad(x[:,4]) #selecting the comments for negative i-flux. there are 40
    e=bad(x[:,2]) #selecting the comments for negative g-flux. there are 21
    
#u g r i z
    