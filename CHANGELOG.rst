CHANGELOG
=========

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