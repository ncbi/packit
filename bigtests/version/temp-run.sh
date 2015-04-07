#!/bin/bash

echo "This doesn't test the values of the outputs, you have to do that yourself sorry"
echo
echo "It's just until the entire packit tool works"
echo

for D in *; do
    if [ ! -d $D ]; then
        continue
    fi
    (
        cd $D;
        echo $D;
        PATH=.:$PATH python ../temp-test-run.py
    )
done
