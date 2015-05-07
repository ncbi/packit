# -*- coding: utf-8 -*-
# Author: Douglas Creager <dcreager@dcreager.net>
# This file is placed into the public domain.

# Calculates the current version number.  If possible, this is the
# output of "git describe", modified to conform to the versioning
# scheme that setuptools uses.  If "git describe" returns an error
# (most likely because we're in an unpacked copy of a release tarball,
# rather than in a git working copy), then we fall back on reading the
# contents of the PKG-INFO or METADATA files in sdists or wheels,
# respectively.
from __future__ import print_function

from distutils import log
from subprocess import Popen, PIPE


__all__ = "git_pep440_version_generator",


DEFAULT_TEMPLATE = "{tag}.post{distance}+{hash}"


def git_pep440_version_generator(template):
    if not template:
        template = DEFAULT_TEMPLATE

    description = call_git_describe()
    if not description:
        return None

    version_info = parse_git_describe(description)

    # For versions that are tagged, just use the tag.
    if not version_info['distance'] and not version_info['hash']:
        return version_info['tag']

    return template.format(**version_info)


def call_git(*params):
    # Might throw OSError if git isn't on the path.
    try:
        p = Popen(('git', ) + params, stdout=PIPE)
    except OSError as ex:
        log.fatal("[git-pep440] Cannot call git... Are you sure git is on sys path?")
        raise SystemExit(ex.errno)

    result = b'\n'.join(p.stdout.readlines())
    p.wait()

    return result.strip().decode('utf-8')


def call_git_describe():
    result = call_git('describe')

    if not result:
        log.fatal("[git-pep440] The 'git describe' output is empty. Are you sure you have tags?")
        raise SystemExit(1)

    return result


def parse_git_describe(description):
    description_tokens = description.rsplit('-', 2)
    tag, distance, hash_val = (description_tokens + ['']*2)[:3]

    hash_val = hash_val[1:]

    return dict(tag=tag, distance=distance, hash=hash_val)
