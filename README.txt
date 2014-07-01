to run the Tractor on a galaxy:
-in the tractor directory, clone it here: <svn link? or https://github.com/dstndstn/tractor>
    - you will also need to access tools in astrometry, acquire by: <svn co svn+ssh://astrometry.net/svn/trunk/src/astrometry/> <make> <make py>
-run generalRC3() from general.py on some source RC3 data (can be downloaded from http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=VII/155)
-alternatively generalNSAtlas() can be used on NSA source data (found here http://nsatlas.org/data)
-the respective functions in general.py will automatically generate flipbooks for each galaxy and a pickle file containing position and CG components
-to measure the halflight values, run halflight.py by specifying the directory of the pickle output files from the Tractor
-to measure the halflight values using a mixture of the data and the model, run wcsimage.py with the i-band fits file created by sloan_atlas.pro. 
    -note that about 100 objects were not measured with this method due to large image size. see notes/no_geomean_output.txt for specific galaxies

to create a fits table from '*-updated.pickle' files (output by halflight.py):
-run create_fits.py providing a list of directions in which all desired pickle files are contained
-create_fits.py also contains function to sort the table and cut the table on specific values 

to assign quantile integers and make image webpages:
-the input to choose_quantile.py will be the table created in create_fits.py and the desired number of cuts in color(g-i) and surfacebrightness
-choose_quantile will assign quantile integers and rebuild the input table, now including a 'QUANTILE' column
-for webpages:in the same directory as sloan_atlas.pro and the input table, run make_quantiles.py with the specified number of quantiles input in choose_quantile.py
-sloan_atlas.pro was run on bootes in /global/data/scr/dhw3/ep109

note-taking methods and post-processing:
-the allnotes.tex files was compiled at various points along the timeline of this project
-miscellaneous notes were taken as subsets of our sample of galaxies were run, especially in the process of checking that NSA galaxies were also being well fit despite possible inaccurately reported sizes by NSA
-the first round of notes were taken once the full sample was finished
     - we plotted g-i vs. surface brightness in the i-band and manually drew a line to the right of the dense cluster and began to observe the flibooks of galaxies that were outliers 
     - these outliers were rerun if they appeared to be mergers, galaxy pairs, or had fits initialized off-center with the galaxy nucleus
-the second round of notes were taken after the quantiles were created
     - each quantile webpage was observed and any abnormalities in ordering or image quality were noted, especially if the galaxy had a very wrong color or size compared to the others in the same quantile
-the last set of notes were taken on a final pass through the same g-i vs. surface brightness plot, where the outliers from the first round were rerun and replotted with new values
     - all outliers were rerun until they fell on the dense area of the plot, or until they were confirmed to be truly low surface brightness galaxies
-miscellaneous notes were adding individually as well

to run The Tractor while switching Exp and deV profiles:
-run newCG.py on the desired galaxies
-if the loglikelihood is greater after the second round of optimization that it was in the first round, a new flipbook and pickle file will be generated

extinction:
-we take our extinction values from the SFD dust map, you must possess SFD_dust_4096_ngp.fits and SFD_dust_4096_sgp.fits to incorporate extinctions 
-calculating corrections requires these extinction values, listed by filter:     
    sloanu=5.155
    sloang=3.793
    sloanr=2.751
    sloani=2.086
    sloanz=1.479
and also the astropysics package to calculate galactic coordinates, which are input into the get_SFD_dust() function
-note: the Tractor does not output extinction-corrected magnitudes; subtract the 'CG_EXTINCTION' column from 'CG_TOTMAGS' 

a note on pickle files:
- <galaxy name>.pickle is output by Tractor fits
- <galaxy name>-updated.pickle contains above and r50 and r90 values (halflight.py output)
- <galaxy name>-updated2.pickle contains above and h50 and h90 values (halflight.py output)
- <galaxy name>_geomean.pickle contains above h50 and h90 values measured on mixture of data + model (wcsimage.py output)
