#!/bin/bash

cd "`dirname $0`"

if ! python -c 'import packman'; then
	echo "Run the test suite inside a virtualenv with packman, please"
	exit 1
fi

ANY_FAILS=0

for runner in */*/run.sh; do
	dir=`dirname $runner`
	echo -n $dir ...
	(cd $dir; ./run.sh)
	if [ $? -eq 0 ]; then
		echo "OK"
	else
		echo "FAIL"
		ANY_FAILS=1
	fi
	echo
done

echo
echo

if [ $ANY_FAILS -eq 0 ]; then
	echo "All passed, how elite"
else
	echo "Some fails, better luck next time"
fi

exit $ANY_FAILS
