CHANGELOG
=========

0.12 (26 Oct 2015)
------------------

- API: '--additional-test-args' replaced '--test-args' in PacKit's test command

- Bugfix: setuptools 18.4 compatibility

0.11 (7 Oct 2015)
-----------------

- Improvement: glob (and globstar) support in [files]/extra_files

- Improvement: glob (and globstar) support in [files]/scripts

- Improvement: include all files referenced in data_files into extra_files

- Improvement: git-pep440 reports version 0.0 when there are no tags or git repo doesn't exist

- Bugfix: '-r' syntax in requirements files - referenced files now included properly


0.10 (7 July 2015)
------------------

- Improvement: Improved PBR compatibility - PacKit works with PBR versions
  greater than 0.10 and lower than 2.0 (presumably)

0.9.2 (15 Jun 2015)
-------------------

- Improvement: updated licensing information in package meta-data. License set
  to 'Public Domain', added 'License :: Public Domain' classifier and
  'LICENSE.txt' included into MANIFEST.in

0.9.1 (10 Jun 2015)
-------------------

- Bugfix: crash on 'python setup.py test' (without additional parameters)
  due to wrong shlex usage


0.9 (10 Jun 2015)
-----------------

- Bugfix/Improvement: glob (and globstar) support in [files]/data-files

- Bugfix: proper parameters passing to tox with -a/--test-args=

0.8 (02 Jun 2015)
-----------------

- Improvement: added 'composite' version strategy

- Improvement: added 'output' option into auto-version configuration

0.7 (21 May 2015)
-----------------

- Bugfix: missing extra files when installing from sdist made with PacKit

- Bugfix: requirements not installed when installing from sdist made with
  PacKit

- Improvement: added contact information to PacKit metadata

0.6 (14 May 2015)
-----------------

- Fixed bug: unspecified packages_root makes nested packages top-level

- Proper handling of 'packages_root = .'

- Updated tox version to ~=2.0, pytest~=2.7, teamcity-messages~=1.12 and
  pytest-gitignore~=1.1

0.5.1 (07 May 2015)
-------------------

- Fixed TypeError in git-pep440 versioning strategy

0.5 (07 May 2015)
-----------------

- Better error handling for git-pep440 versioning strategy

- Now PacKit honors only 'index_url' and 'find_links' PIP fetch directives but
  looks for them not only in env vars but also in PIP configuration files as
  per PIP docs (requires PIP at least 1.5.0)

0.4 (05 May 2015)
-----------------

- Improved PacKit's test command - skip dependencies install when running tox,
  honor PIP's fetch directives

0.3 (04 May 2015)
-----------------

- Fixed TypeError on Python 2 due to several instances of setuptools being
  loaded at the same time

- PacKit forces easy_install to honor PIP's fetch directives set through
  environment variables

- Normalized post-version formatting from '-{num}' to '.post{num}' for
  Git-PEP440 versioning strategy


0.2 (28 Apr 2015)
-----------------

- Workaround for "dist must be a Distribution instance" bug
  (https://bugs.launchpad.net/pbr/+bug/1412875)


0.1 (15 Apr 2015)
-----------------

- Initial release
