to run the Tractor on a galaxy:
-in the tractor directory, clone it here: <svn link? or https://github.com/dstndstn/tractor>
    - you will also need to access tools in astrometry, acquire by: <svn co svn+ssh://astrometry.net/svn/trunk/src/astrometry/> <make> <make py>
-run generalRC3() from general.py on some source RC3 data (can be downloaded from http://vizier.u-strasbg.fr/viz-bin/VizieR?-source=VII/155)
-alternatively generalNSAtlas() can be use on NSA source data (found here http://nsatlas.org/data)
-the respective functions in general.py will automatically generate flipbooks for each galaxy
-to measure the halflight values, run halflight.py by specifying the location of the pickle output files from the Tractor

to create a fits table from '*-updated.pickle' files (output by halflight.py):
-run create_fits.py once for the RC3 galaxies and once for the NSA galaxies
-combine_fits.py will combine the two tables into one, also allowing for a lower radius cut and ordering parameter to be set
-combine_fits.py will not contain quantile integers, see choose_quantiles.py to generate desired integers

to make quantiles:
-this will require an input table that has some integer value assigned to each galaxy; see choose_quantile.py to generate one
-in the same directory as sloan_atlas.pro and the input table, run make_quantiles.py with the specified number of quantiles input in choose_quantile.py
-ran all quantile making processes bootes in /global/data/scr/dhw3/ep109

making notes:
-the allnotes.tex files was compiled at various points along the timeline of this project
-miscellaneous notes were taken as subsets of our sample of galaxies were run, especially in the process of checking that NSA galaxies were also being well fit despite possible inaccurately reported sizes by NSA
-the first round of notes were taken once the full sample was finished
     - we plotted g-i vs. surface brightness in the i-band and manually drew a line to the right of the dense cluster and began to observe the flibooks of galaxies that were outliers 
     - these outliers were rerun if they appeared to be mergers, galaxy pairs, or had fits initialized off-center with the galaxy nucleus
-the second round of notes were taken after the quantiles were created
     - each quantile webpage was observed and any abnormalities in ordering or image quality were noted, especially if the galaxy had a very wrong color or size compared to the others in the same quantile
-the last set of notes were taken on a final pass through the same g-i vs. surface brightness plot, where the outliers from the first round were rerun and replotted with new values
     - all outliers were rerun until they fell on the dense area of the plot, or until they were confirmed to be truly low surface brightness galaxies

to run The Tractor while switching Exp and deV profiles:
-run newCG.py on the desired galaxies
-if the loglikelihood is greater after the second round of optimization that it was in the first round, a flipbook will be generated

a note on extinction:
-we take our extinction values from the SFD dust map, you must possess SFD_dust_4096_ngp.fits and SFD_dust_4096_sgp.fits to incorporate extinctions into a final Atlas table
-calculating corrections requires these extinction values by filter:     
    sloanu=5.155
    sloang=3.793
    sloanr=2.751
    sloani=2.086
    sloanz=1.479
and also the astropysics package to calculate galactic coordinates, which are input into the get_SFD_dust() function
-our values are not extinction corrected directly from the Tractor and that they must be manually calculated by subtracting the values in the  'EXTINCTION' column
