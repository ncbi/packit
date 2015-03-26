#!/bin/sh -e
source ../../assert.sh

assert "python setup.py --version" 1.3.3

assert_end version/git-release
