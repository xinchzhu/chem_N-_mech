#!/bin/bash

for ID in {0..20}
do
    cd ./irc_files/RPHt_$ID/
    RPHt2.exe
    cd ..
    cd ..
done
