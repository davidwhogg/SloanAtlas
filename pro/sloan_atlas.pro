;+
; NAME:
;   sloan_atlas
; PURPOSE:
;   Make fits mosaics, jpgs, pngs, and html for Sloan Atlas galaxies
; INPUTS:
; OPTIONAL INPUTS:
;   suffix  - add this suffix to file names
;   columns - set the number of columns in the html table (default 6)
;   maxgal  - maximum number of plates to make.
;   quantile - chooses galaxies with only this quantile number,
;              integer 0-15
; KEYWORDS:
; OUTPUTS:
; OPTIONAL OUTPUTS:
; DEPENDENCIES:
;   idlutils
;   photoop
; BUGS:
;   - FIND ALL "HOGG" NOTES IN CODE.
;   - Needs to make PNGs not JPEGs.
;   - Needs to embiggen PNGs by factor 8x8 or so.
;   - Need to run "setup tree bosswork" in the shell, or sommat like that.
;   - Stuff hard-coded.
; REVISION HISTORY:
;   2005-01-26  started - Hogg
;   2011-09-08  updated to DR8 - Hogg (with help from Weaver)
;   2013-02-23  began branch to Sloan Atlas - Hogg
;   2013-07-22  moved to github - Hogg
;-
pro sloan_atlas, suffix=suffix,columns=columns,maxgal=maxgal,quantile=quantile

; set defaults
nxpix= 1024
nypix= 1024
rebinfactor= 2
if (~keyword_set(columns)) then columns = 6L
; clean up the old
cmd= 'find -mmin +1440 -empty -exec \rm -fv \{} \;'
splog, cmd
spawn, cmd

;start webpage
openw, wlun,'index.'+getenv('SHORTHOST')+'.html',/get_lun
printf, wlun,'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">'
printf, wlun,'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">'
printf, wlun,'<head>'
printf, wlun,'<title>Hogg / SDSS images of selected Sloan Atlas galaxies</title>'
printf, wlun,'<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
printf, wlun,'<style type="text/css" media="screen">'
printf, wlun,'table { font-size: 75%; }'
printf, wlun,'td { vertical-align: top; }'
printf, wlun,'</style>'
printf, wlun,'</head>'
printf, wlun,'<body>'
printf, wlun,'<h1>SDSS images of selected Sloan Atlas galaxies</h1>'
printf, wlun,'<p>The mosaics are custom-built out of raw <i>SDSS</i> and <i>SDSS-III</i> data at NYU.'
printf, wlun,'   They are all north-up.  Send questions or comments to'
printf, wlun,'   <a href="http://cosmo.nyu.edu/hogg/">David&nbsp;W.&nbsp;Hogg</a>.</p>'
printf, wlun,'<p><i>Warning:</i> Some images contain significant'
printf, wlun,'   data artifacts.  For example, we have not restricted the'
printf, wlun,'   sample to those overlapping <q>survey quality</q> SDSS data.'
printf, wlun,'   Use at your own risk.</p>'
printf, wlun,'<p>Attribution for these images ought to be, at least,'
printf, wlun,'   <q>David&nbsp;W.&nbsp;Hogg and the'
printf, wlun,'      Sloan Digital Sky Survey Collaborations</q>.</p>'
printf, wlun,'<p><i>All images are &copy; 2013 David W. Hogg.</i></p>'
printf, wlun,'<table>'

; read in and loop over input data
table_rows = ['foo']
tabfilename = './sdss_atlas_for_images_all.fits' 
tab = mrdfits(tabfilename, 1)
print, tag_names(tab)

if keyword_set(maxgal) then ngal = ngal < maxgal
;tab = tab[sort(tab.cg_r50s[3])]
tab=tab[reverse(sort(tab.cg_r90s[3]))]
q=WHERE(tab.quantile EQ quantile)
tab = tab(q)
;print, n_elements(tab)
ngal = n_elements(tab)
ii= 0
for j=0L,ngal-1L do begin
    thistab= tab[j]
;    print,j, thistab.name
;    CONTINUE


;;; HOGG FIXME!
; set pixscale and image size
    pixscale= (0.396 / 3600.) / rebinfactor
    ra_size= float(nxpix)*rebinfactor*pixscale
    dec_size= ra_size*float(nypix)/float(nxpix)
    splog, 'ra_size ',ra_size
    splog, 'dec_size ',dec_size
    splog, 'pixscale', pixscale

; make names and title
    splog, 'names ',thistab.name
    shortname1= thistab.name
    shortname1= strjoin(strsplit(shortname1,' ',/extract),' ',/single)
    title= shortname1 + ' / ' + hogg_iau_name(thistab.cg_ra,thistab.cg_dec,'SA')
    splog, 'title is '+title

; make prefix
    prefix= strjoin(strsplit(title,'/',/extract),' ',/single)
    prefix= strjoin(strsplit(prefix,' ',/extract),'_',/single)
    if keyword_set(suffix) then prefix= prefix+'_'+suffix
    splog, 'prefix is '+prefix

; smosaic make
    bigast= 0                   ; reset astrom
    rerun= 301                  ; current best rerun?
    filename= 0                 ; reset names
    cleanname= 0
    hardname= 0
    smosaic_make_jpg, thistab.cg_ra, thistab.cg_dec, ra_size, dec_size, $
      filename, astrans=bigast, prefix=prefix, $
      pixscale=pixscale, smfwhm=pixscale*2.0*3600.0, $
      rebinfactor=rebinfactor, title=title, $
      npixround=8, cleanname=cleanname, hardname=hardname, /nogrid, $
      quality=99, /dontdelete, /ivarout, /dontcrash, $
      minscore=0.5, /ignoreframesstatus, /processed, rerun=rerun, $
      /global, /dropweights

; check file size
    dot = strpos(filename,'.jpg',/reverse_search)
    info = file_info(filename)
    IF (info.size eq 0) THEN BEGIN
        ;;;; HOGGG WE SHOULD DIE HERE
        cmd = '\rm '+filename+' '+strmid(filename,0,dot)+'*.jpg'
        spawn,cmd
    ENDIF ELSE BEGIN

; make different versions
        thumbimage = strmid(filename,0,dot)+'_thumb.jpg'
        scalefactor= string(128.0/float(nxpix))
        cmd1 = "anytopnm "+filename+" | pnmscale " $
          +scalefactor+" | ppmtojpeg > "+thumbimage
        splog, cmd1
        spawn, cmd1

; check thumb for blackness
        read_jpeg, thumbimage,bad,true=3
        zero= where(bad EQ 0,nzero)
        zerofrac= float(nzero)/float(n_elements(bad))
        if (zerofrac GT 0.35) then begin
            ;;;; HOGG WE SHOULD DIE HERE
        endif

        halfsize = strmid(filename,0,dot)+'_halfsize.jpg'
        cmd2 = "anytopnm "+filename+" | pnmscale 0.5 | ppmtojpeg > "+ $
          halfsize
        splog, cmd2
        spawn, cmd2

        ii= (ii+1) MOD columns
        htmlname= strjoin(strsplit(title,' ',/extract,/regex), $
                          '&nbsp;',/single)
        htmlname= strjoin(strsplit(htmlname,'&nbsp;\/&nbsp;',/extract,/regex), $
                          '<br />',/single)
        splog, 'htmlname is '+htmlname
        table_row = '<td><a href="'+filename+'"><img src="'+ $
          thumbimage+'" alt="[image]" /></a>' + $
          '<br /><a href="'+filename+'">labeled</a>' + $
          '&nbsp;-&nbsp;<a href="'+cleanname+'">unlabeled</a>' + $
          '<br /><a href="'+halfsize+'">half&nbsp;size</a>' + $
          '&nbsp;-&nbsp;<a href="'+hardname+'">hard&nbsp;stretch</a>' + $
          '<br />'+htmlname+'</td>'
        table_rows = [table_rows, table_row]
        flush, wlun
    endelse
endfor

; write out table rows
if (n_elements(table_rows) GT 1) then begin
    table_rows = table_rows[1:n_elements(table_rows)-1]
endif
while ( (n_elements(table_rows) MOD columns) NE 0 ) do table_rows = [table_rows, '<td></td>']
for k = 0L, (n_elements(table_rows)/columns)-1L do begin
    printf, wlun, '<tr>'
    printf, wlun, strjoin(table_rows[k*columns:((k+1L)*columns-1L)],string(10b))
    printf, wlun, '</tr>'
endfor

; close up and finish
printf, wlun, '</table>'
printf, wlun, '</body>'
printf, wlun, '</html>'
close, wlun
free_lun, wlun

; clean up the zero-length crap
cmd= 'find -empty -exec \rm -fv \{} \;'
splog, cmd
spawn, cmd
return
end
