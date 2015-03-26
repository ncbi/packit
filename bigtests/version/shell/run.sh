#!/bin/sh -e
source ../../assert.sh

assert "python setup.py --version" 2.22.2

assert_end version/shell
