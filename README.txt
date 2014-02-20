to run the Tractor on a galaxy:
-in the tractor directory, <svn link? or https://github.com/dstndstn/tractor>
-run generalRC3() from general.py on some source RC3 data
-alternatively generalNSAtlas() can be use on NSA source data
-to measure the halflight values, run halflight.py by specifying the location of the pickle output files from the Tractor

to create a fits table from -updated.pickle files output by halflight.py:
-run create_fits.py once for the RC3 galaxies and once for the NSA galaxies
-combine_fits.py will combine the two tables into one, also allowing for a lower radius cut and ordering parameter to be set
-combine_fits.py will not contain quantile integers, see choose_quantiles.py to generate desired integers

to make quantiles:
-run sloan_atlas.pro on bootes in /global/data/scr/dhw3/ep109
-this will require an input table that has some integer value assigned to each galaxy; see choose_quantile.py

