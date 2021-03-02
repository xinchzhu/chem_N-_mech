perform JSR simualtion with Cantera code
./1_sim_JSR.py should be modified for different conditions
Molefractions for all species as functions of time (timehistory) are written in ./timhis_JSR_xxx.dat where xxx are temperatures simualted
timehistory for specific species can be defined in ./1_sim_JSR.py spript and written in ./timhis_JSR_xxx_sorted_O2.csv along with plotted figure in the same directory

Cautious:
Molefractions for reactants may not converge as calculation proceeds, thus, timehistory for O2 are displayed on screen after each run to confirm the convergency of X_O2
