# binned
We run a series of programs to generate binned drifter statistics as follows:

1. run segment.py to get the individual files one for each drifter 

2. run S0_1hr.py to get hourly data and remove tide 

3. run S1_mean.py to bin the velocities 

4. run S2_plot.py to plot vectors
