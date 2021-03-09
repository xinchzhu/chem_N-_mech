#!/bin/bash

dir=$(pwd)
cp /home/zxc/Documents/gauss2RPHt/bin/1_RHPt_writer_sep.py  $dir
cp /home/zxc/Documents/gauss2RPHt/bin/2_energy_reader.py  $dir
cp /home/zxc/Documents/gauss2RPHt/bin/3_mess_writer.py  $dir
cp /home/zxc/Documents/gauss2RPHt/bin/2_run_RPHt_run_all.sh  $dir

echo 'Reading irc.log file' ;
python 1_RHPt_writer_sep.py;
echo 'Generated Hessian, gradient, geomerty and energy files for each steps';
echo 'Converting energy:';
python 2_energy_reader.py;
echo 'Running RHPt.exe'
bash 2_run_RPHt_run_all.sh > autolog.log ; 
echo 'writing input for MESS:'
python 3_mess_writer.py

