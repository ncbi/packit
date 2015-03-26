#!/bin/sh -e
source ../../assert.sh

assert "python setup.py --version" 1.3.3.post7+g00d

assert_end version/git-non-release
