CHANGELOG
=========

0.5.1 (07 May 2015)
-------------------

- Fixed TypeError in git-pep440 versioning strategy

0.5 (07 May 2015)
-----------------

- Better error handling for git-pep440 versioning strategy

- Now PacKit honors only 'index_url' and 'find_links' PIP fetch directives but looks for them not only in
  env vars but also in PIP configuration files as per PIP docs (requires PIP at least 1.5.0)

0.4 (05 May 2015)
-----------------

- Improved PacKit's test command - skip dependencies install when running tox, honor PIP's fetch directives

0.3 (04 May 2015)
-----------------

- Fixed TypeError on Python 2 due to several instances of setuptools being loaded at the same time

- PacKit forces easy_install to honor PIP's fetch directives set through environment variables

- Normalized post-version formatting from '-{num}' to '.post{num}' for Git-PEP440 versioning strategy


0.2 (28 Apr 2015)
-----------------

- Workaround for "dist must be a Distribution instance" bug (https://bugs.launchpad.net/pbr/+bug/1412875)


0.1 (15 Apr 2015)
-----------------

- Initial release
