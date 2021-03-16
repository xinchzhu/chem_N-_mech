#!/bin/bash

for ID in {0..20}
do
    cd ./irc_files/RPHt_$ID/
    RPHt.exe
    cd ..
    cd ..
done
