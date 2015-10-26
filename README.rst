PacKit
======

Rationale
---------

Creating python packages is routine operation that involves a lot of
actions that could be automated. Although there are petty good tools
like `pbr`_ for that purpose, they miss some features and lack
flexibility by trying to enforce some strongly opinionated decisions
upon you.  PacKit tries to solve this by providing a simple,
convenient, and flexible way to create and build packages while aiming
for following goals:

- simple declarative way to configure your package through ``setup.cfg`` following  `distutils2 setup.cfg syntax`_

- reasonable defaults

- open for extension

Overview
--------

PacKit is wrapper around `pbr`_ though it only uses it for interaction
with setuptools/distutils through simplified interface.  None of `pbr`_
functions are exposed but instead PacKit provides its own
interface.

Available facilities
^^^^^^^^^^^^^^^^^^^^

Here's a brief overview of currently implemented facilities and the
list will be extended as new ones will be added.

- **auto-version** - set package version depending on selected
  versioning strategy.

- **auto-description** - set package long description

- **auto-license** - include license file into distribution

- **auto-dependencies** - populate ``install_requires`` and
  *test_requires* from requirement files

- **auto-packages** - discover packages to include in distribution.

- **auto-extra-meta** - add useful options to the metadata config section

- **auto-package-data** - include all files tracked by ``git`` from
  package dirs only.

- **auto-tests** - make ``python setup.py test`` run tests with ``tox``
  or ``pytest`` (depending on ``tox.ini`` presence).

On top of that PacKit forces easy_install to honor following `PIP's fetch directives`_:

- index_url

- find_links


Planned facilities
^^^^^^^^^^^^^^^^^^

- **auto-plate** - integration with `platter`_

- **auto-license** - fill out license information

- **auto-pep8** - produce style-check reports

- **auto-docs** - API docs generation

- **auto-clean** - configurable clean jobs

- **auto-coverage** (?) - produce coverage reports while running tests

If you don't see desired facilities or have cool features in mind feel
free to contact us and tell about your ideas.


Usage
-----

Create a ``setup.py`` in your project dir:
::

    from setuptools import setup

    setup(setup_requires='packit', packit=True)


That was the first and the last time you touched that file for your project.

Now let's create a ``setup.cfg`` that you will use in order to configure
your package:

::

    [metadata]
    name = cool-package


And... if you're not doing anything tricky in your package then that's
enough! And if you do, take a look at the section below.


Facilities
----------

Currently all available facilities are enabled by default. Though you
can easily turn them off by using ``facilities`` section in your
``setup.cfg``:

::

    [facilities]
    auto-version = 0
    auto-dependencies = f
    auto-packages = false
    auto-package-data = n
    auto-tests = no


If facility is explicitly disabled it won't be used even if
facility-specific configuration section is present.

Facility-specific defaults and configuration options described below.


auto-version
^^^^^^^^^^^^

When enabled, ``auto-version`` will generate and set package version
according to selected versioning strategy.

Versioning strategy can be selected using ``type`` field under
``auto-version`` section within ``setup.cfg``.  The default is:

::

    [auto-version]
    type = git-pep440
    output = src/templates/version.html


You can use ``output`` field to ask PacKit to write generated version value
into specified filename. The specified filename do not need to exist but the
parent directories should exist. Provided path should always use
forward slashes.

git-pep440
""""""""""

Generate `PEP440`_-compliant version from ``git`` tags. It's expected
that you using git tags that follow `public version identifier`_
description and ``git-pep440`` will just append number of commits since
tag was applied to your tag value (the ``N`` in `public version
identifier`_ description).

If number of commits since tag equal to 0 (your building the tagged
version) the ``N`` value won't be appended. Otherwise, it will be
appended and `local version identifier`_ equal to first 7 chars of
commit hash will be also added.

Example:
1. <git tag 1.2.3.dev> -> version is ``1.2.3.dev``

2. <git commit> -> version is ``1.2.3.dev.post1``

3. <git commit> -> version is ``1.2.3.dev.post2``

4. <git tag 1.2.3.a> -> version is ``1.2.3.a``

5. <git commit> -> version is ``1.2.3.a.post1``

6. <git tag 1.2.3> -> version is ``1.2.3``

7. <git commit> -> version is ``1.2.3.post1``

8. <git commit> -> version is ``1.2.3.post2``

fixed
"""""

Use value specified in ``value`` (it's required when this strategy is
used) under ``auto-version`` section in ``setup.cfg``:

::

    [auto-version]
    type = fixed
    value = 3.3

file
""""

Read a line using UTF-8 encoding from the file specified in ``value``
(it's required when this strategy is used) under ``auto-version``
section in ``setup.cfg``, strip it and use as a version.

::

    [auto-version]
    type = file
    value = VERSION.txt

shell
"""""

Execute command specified in ``value`` (it's required when this strategy
is used) under ``auto-version`` section in ``setup.cfg``, read a line from
``stdout``, strip it and use as a version

composite
"""""""""

The most advanced version strategy designed for special cases. It allows you
to generate complex version values based on other version strategies. The
usage is pretty simple though:

::

    [auto-version]
    type = composite
    value = {foo}.{bar}+{git}
    output = main.version

    [auto-version:foo]
    type = fixed
    value = 42
    output = 1st.version

    [auto-version:bar]
    type = shell
    value = echo $RANDOM

    [auto-version:git]
    type = git-pep440
    output = 3rd.version

The ``value`` field in composite version strategy should be a valid
`string format expression`_.

Please note that ``output`` directives used here only for reference (to show
that they can be used anywhere) and are not required.

It's OK to define 'extra' version components and not use them but it's an
error to not define any of components mentioned in composite version template.

auto-description
^^^^^^^^^^^^^^^^

When enabled will fill out ``long_description`` for package from a readme.

The ``readme`` file name could be specified with ``file`` field under
``auto-description`` section.

If no file name provided, it will be discovered automatically by
trying following list of files:

- README

- readme

- CHANGELOG

- changelog

Each of these files will be tried with following extensions:

- <without extension>

- .md

- .markdown

- .mkdn

- .text

- .rst

- .txt

The readme file will be included in the package data.

auto-license
^^^^^^^^^^^^

When enabled will include the license file into the distribution.

The license file name could be specified by the ``file`` field within ``auto-license`` section.

If license file name is not provided the facility will try to discover it in the current dir
trying following file names:

- LICENSE

- license

Each of these files will be tried with following extensions:

- <without extension>

- .md

- .markdown

- .mkdn

- .text

- .rst

- .txt

auto-dependencies
^^^^^^^^^^^^^^^^^

When enabled will fill ``install_requires`` and ``test_requires`` from requirement
files.

Requirement files could be specified by ``install`` and ``test`` fields under
the ``auto-dependencies`` section of the ``setup.cfg``.

If requirements file names not provided then the facility will try to discover them automatically.

For installation requirements following paths will be tried:

- requires
- requirements
- requirements/prod
- requirements/release
- requirements/install
- requirements/main
- requirements/base

For testing requirements following paths will be tried:

- test-requires
- test_requires
- test-requirements
- test_requirements
- requirements_test
- requirements-test
- requirements/test

For each path following extensions will be tried

- <without extension>
- .pip
- .txt

Once a file is found, PacKit stops looking for more files.

**You can use vcs project urls and/or archive urls/paths** as
described in `pip usage`_ - they will be split in dependency links and
package names during package creation and will be properly handled by
pip/easyinstall during installation.  Remember that you can also make
"includes" relationships between ``requirements.txt`` files by
including a line like ``-r other-requires-file.txt``.

auto-packages
^^^^^^^^^^^^^

When enabled and no packages provided in ``setup.cfg`` through
``packages`` option under ``files`` section will try to automatically find
out all packages in current dir recursively.

It operates using ``exclude`` and ``include`` values that can be specified
under ``auto-packages`` section within ``setup.cfg``.

If ``exclude`` not provided the following defaults will be used:
``test``, ``docs``, ``.tox`` and ``env``.

If ``include`` not provided, ``auto-packages`` will try the following
steps in order to generate it:

1. If ``packages_root`` value provided under ``files`` section in
   ``setup.cfg``, it will be used.

2. Otherwise the current working dir will be scanned for any python
   packages (dirs with __init__.py) while honoring exclude
   ``value``. *This packages also will be included into the resulting
   list of packages.*

Once ``include`` value is determined, the resulting packages list will
be generated using following algorithm:

::

  for path in include:
      found_packages |= set(find_packages(path, exclude))


auto-extra-meta
^^^^^^^^^^^^^^^

When enabled, adds a number of additional options to 'metadata' section.

Right now, only 1 extra option supported:

- **is_pure** - allows you to override 'purity' flag for distribution, i.e.
  you can explicitly say whether your distribution is platform-specific or no.


auto-package-data
^^^^^^^^^^^^^^^^^

When enabled:

1. If the ``everything`` option under the ``auto-package-data`` section is
    set to true, behaves like `setuptools-git`_. Otherwise, includes all
    files only from packages' dirs tracked by git to distribution.

2. Allows you to specify extra files to be included in distribution in
   ``setup.cfg`` using ``extra_files`` under ``files`` section like:

::

  [files]
  extra_files =
    LICENSE.txt
    hints.txt
    some/stuff/lib.so

3. Allows you to use glob syntax (including globstar) in ``data-files``, ``extra_files`` and ``scripts``

auto-tests
^^^^^^^^^^

Has no additional configuration options [yet].

When enabled, the ``python setup.py test`` is equal to running:

- **tox** if ``tox.ini`` is present

- **pytest** with `pytest-gitignore`_ and `teamcity-messages`_ plugins
  enabled by default otherwise (if you need any other plugins just add
  them to test requirements) and activate them with additional options
  (see below)

The facility automatically downloads underlying test framework and install
it - you don't need to worry about it.

You can pass additional parameters to the underlying test framework with
'-a' or '--additional-test-args='.

Further Development
-------------------

- Add tests
- Improve docs
- More configuration options for existing facilities
- New facilities
- Allow extension through entry points


.. _pbr: http://docs.openstack.org/developer/pbr/
.. _distutils2 setup.cfg syntax: http://alexis.notmyidea.org/distutils2/setupcfg.html
.. _PIP's fetch directives: https://pip.pypa.io/en/latest/user_guide.html#configuration
.. _platter: http://platter.pocoo.org/
.. _setuptools-git: https://pypi.python.org/pypi/setuptools-git
.. _pytest-gitignore: https://pypi.python.org/pypi/pytest-gitignore/
.. _teamcity-messages: https://pypi.python.org/pypi/teamcity-messages/
.. _pip usage: https://pip.pypa.io/en/latest/reference/pip_install.html#usage
.. _PEP440: https://www.python.org/dev/peps/pep-0440/
.. _public version identifier: https://www.python.org/dev/peps/pep-0440/#public-version-identifiers
.. _local version identifier: https://www.python.org/dev/peps/pep-0440/#local-version-identifiers
.. _string format expression: https://docs.python.org/2/library/string.html#string-formatting
