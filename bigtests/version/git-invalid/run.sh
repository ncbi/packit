#!/bin/sh -e
source ../../assert.sh

assert_stderr "python setup.py --version" "ValueError: The version \"asdf1.3.3\" is not PEP440 compliant.  Maybe you have used a git tag which is not something like v1.2.3 or 1.2.3"

assert_end version/git-release
