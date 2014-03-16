import numpy as np
import pyfits as pyf
import os
   
# os.chdir("RC3_Output/")
# os.system('cp large_galaxies_2013.fits ../')
# os.chdir("../")

# os.chdir("NSAtlas_Output/")
# os.system('cp nsa_galaxies_2013.fits ../')
# os.chdir("../")

data=pyf.open('large_galaxies_2013.fits')
data2=data[1].data
cols=data[1].columns
#print cols.names

n=np.arange(100)
hdu=pyf.PrimaryHDU(n)

name=data2.field('RC3_NAME')
#print len(name)
a=data2.field('RC3_RA')
b=data2.field('RC3_DEC')
c=data2.field('RC3_LOG_D25')
d=data2.field('CG_RA')
e=data2.field('CG_DEC')
f=data2.field('CG_R50S')
g=data2.field('CG_R90S')
h=data2.field('CG_CONC')
i=data2.field('CG_TOTMAGS')
j=data2.field('CG_DEVRE')
k=data2.field('CG_DEVAB')
l=data2.field('CG_DEVPHI')
m=data2.field('CG_DEVMAGS')
n=data2.field('CG_EXPRE')
o=data2.field('CG_EXPAB')
p=data2.field('CG_EXPPHI')
q=data2.field('CG_EXPMAGS')
r=data2.field('CG_EXTINCTION')
s=data2.field('CG ISB')
t=data2.field('CG_H50S')
u=data2.field('CG_H90S')

col1=pyf.Column(name='NAME',format='30A',array=name)
col2=pyf.Column(name='ORIGINAL_RA',format='1E',array=a)
col3=pyf.Column(name='ORIGINAL_DEC',format='1E',array=b)
col4=pyf.Column(name='ORIGINAL_R50',format='1E',array=c)
col5=pyf.Column(name='CG_RA',format='1E',array=d)
col6=pyf.Column(name='CG_DEC',format='1E',array=e)
col7=pyf.Column(name='CG_R50S',format='5E',array=f)
col8=pyf.Column(name='CG_R90S',format='5E',array=g)
col9=pyf.Column(name='CG_CONC',format='5E',array=h)
col10=pyf.Column(name='CG_TOTMAGS',format='5E',array=i)
col11=pyf.Column(name='CG_DEVRE',format='1E',array=j)
col12=pyf.Column(name='CG_DEVAB',format='1E',array=k)
col13=pyf.Column(name='CG_DEVPHI',format='1E',array=l)
col14=pyf.Column(name='CG_DEVMAGS',format='5E',array=m)
col15=pyf.Column(name='CG_EXPRE',format='1E',array=n)
col16=pyf.Column(name='CG_EXPAB',format='1E',array=o)
col17=pyf.Column(name='CG_EXPPHI',format='1E',array=p)
col18=pyf.Column(name='CG_EXPMAGS',format='5E',array=q)
col19=pyf.Column(name='CG_EXTINCTION',format='5E',array=r)
col20=pyf.Column(name='CG_ISB',format='1E',array=s)
col21=pyf.Column(name='CG_H50S',format='5E', array=t)
col22=pyf.Column(name='CG_H90S',format='5E',array=u)

columns=pyf.ColDefs([col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14,col15,col16,col17,col18,col19,col20,col21,col22])
tbhdu=pyf.new_table(columns)
tbhdulist=pyf.HDUList([hdu,tbhdu])
tbhdulist.writeto('rc3_combine.fits',clobber=True)

data=pyf.open('rc3_combine.fits')
data2=data[1].data
name=data2.field('NAME')
#print len(name)
cols=data[1].columns
print cols.names

#NSA new table
data=pyf.open('nsa_galaxies_2013.fits')
data2=data[1].data
cols=data[1].columns
n=np.arange(100)
hdu=pyf.PrimaryHDU(n)
name=data2.field('NSA_NAME')
a=data2.field('NSA_RA')
b=data2.field('NSA_DEC')
c=data2.field('NSA_SERSIC_TH50')
d=data2.field('CG_RA')
e=data2.field('CG_DEC')
f=data2.field('CG_R50S')
g=data2.field('CG_R90S')
h=data2.field('CG_CONC')
i=data2.field('CG_TOTMAGS')
j=data2.field('CG_DEVRE')
k=data2.field('CG_DEVAB')
l=data2.field('CG_DEVPHI')
m=data2.field('CG_DEVMAGS')
n=data2.field('CG_EXPRE')
o=data2.field('CG_EXPAB')
p=data2.field('CG_EXPPHI')
q=data2.field('CG_EXPMAGS')
r=data2.field('CG_EXTINCTION')
s=data2.field('CG_ISB')
t=data2.field('NSA_NSID')
u=data2.field('CG_H50S')
v=data2.field('CG_H90S')

col1=pyf.Column(name='NAME',format='30A',array=name)
col2=pyf.Column(name='ORIGINAL_RA',format='1E',array=a)
col3=pyf.Column(name='ORIGINAL_DEC',format='1E',array=b)
col4=pyf.Column(name='ORIGINAL_R50',format='1E',array=c)
col5=pyf.Column(name='CG_RA',format='1E',array=d)
col6=pyf.Column(name='CG_DEC',format='1E',array=e)
col7=pyf.Column(name='CG_R50S',format='5E',array=f)
col8=pyf.Column(name='CG_R90S',format='5E',array=g)
col9=pyf.Column(name='CG_CONC',format='5E',array=h)
col10=pyf.Column(name='CG_TOTMAGS',format='5E',array=i)
col11=pyf.Column(name='CG_DEVRE',format='1E',array=j)
col12=pyf.Column(name='CG_DEVAB',format='1E',array=k)
col13=pyf.Column(name='CG_DEVPHI',format='1E',array=l)
col14=pyf.Column(name='CG_DEVMAGS',format='5E',array=m)
col15=pyf.Column(name='CG_EXPRE',format='1E',array=n)
col16=pyf.Column(name='CG_EXPAB',format='1E',array=o)
col17=pyf.Column(name='CG_EXPPHI',format='1E',array=p)
col18=pyf.Column(name='CG_EXPMAGS',format='5E',array=q)
col19=pyf.Column(name='CG_EXTINCTION',format='5E',array=r)
col20=pyf.Column(name='CG_ISB',format='1E',array=s)
col21=pyf.Column(name='CG_H50S', format='5E', array=u)
col22=pyf.Column(name='CG_H90S', format='5E', array=v)
columns=pyf.ColDefs([col1,col2,col3,col4,col5,col6,col7,col8,col9,col10,col11,col12,col13,col14,col15,col16,col17,col18,col19,col20,col21, col22])
tbhdu=pyf.new_table(columns)
tbhdulist=pyf.HDUList([hdu,tbhdu])
tbhdulist.writeto('nsa_combine.fits',clobber=True)

data=pyf.open('nsa_combine.fits')
#print data[1]
data2=data[1].data
name=data2.field('CG_RA')
print len(name)
cols=data[1].columns
print cols.names


#combine rc3_combine.fits and nsa_combine.fits
os.system('pwd')
t1=pyf.open('rc3_combine.fits')
t2=pyf.open('nsa_combine.fits')
nrows1=t1[1].data.shape[0]
nrows2=t2[1].data.shape[0]
print nrows1,nrows2
nrows=nrows1+nrows2
print nrows
hdu=pyf.new_table(t1[1].columns,nrows=nrows)
print t1[1].columns.names
for name in t1[1].columns.names:
    hdu.data.field(name)[nrows1:]=t2[1].data.field(name)
hdu.writeto('all_galaxies.fits', clobber=True)

#create mask for the data 
t=pyf.open('all_galaxies.fits')
print t[1].columns.names
tbdata=t[1].data
mask=tbdata.field('CG_H50S')[:,3] > 15.0
newtbdata=tbdata[mask]
print len(newtbdata)
hdu=pyf.BinTableHDU(newtbdata)
hdu.writeto('all_galaxies2.fits',clobber=True) #this is the masked table 

#sort table all_galaxies2.fits by r50i size
data=pyf.open('all_galaxies2.fits')
a=data[1].data.field('CG_R50S')[:,3]
b=data[1].data.field('NAME')
print len(a)
sortsize=np.argsort(a)
#sortname=np.argsort(b)
#data=data[1].data[sortname]
data=data[1].data[sortsize]
hdu=pyf.BinTableHDU(data)
hdu.writeto('sdss_atlas_plates.fits', clobber=True)

#check that it formatted correctly
data=pyf.open('sdss_atlas_plates_quants.fits') 
data2=data[1].data
size=data2.field('CG_H50S')
q =data2.field('QUANTILE')
print len(size), q
print size
name=data2.field('NAME')
cols=data[1].columns
print cols.names

