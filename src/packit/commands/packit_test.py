import os
import shlex

from setuptools.command.test import test as TestCommand


class PackitTest(TestCommand):
    command_name = 'test'

    requirements_tox = [
        'tox~=2.0',
    ]

    requirements_pytest = [
        'pytest~=2.7',
        'teamcity-messages~=1.12',
        'pytest-gitignore~=1.1',
    ]

    def __init__(self, dist, **kw):
        self.distribution = dist
        self.initialize_options()

        # Per-command versions of the global flags, so that the user can
        # customize Distutils' behaviour command-by-command and let some
        # commands fall back on the Distribution's behaviour.  None means
        # "not defined, check self.distribution's copy", while 0 or 1 mean
        # false and true (duh).  Note that this means figuring out the real
        # value of each flag is a touch complicated -- hence "self._dry_run"
        # will be handled by __getattr__, below.
        # XXX This needs to be fixed.
        self._dry_run = None

        # verbose is largely ignored, but needs to be set for
        # backwards compatibility (I think)?
        self.verbose = dist.verbose

        # Some commands define a 'self.force' option to ignore file
        # timestamps, but methods defined *here* assume that
        # 'self.force' exists for all commands.  So define it here
        # just to be safe.
        self.force = None

        # The 'help' flag is just used for command-line parsing, so
        # none of that complicated bureaucracy is needed.
        self.help = 0

        # 'finalized' records whether or not 'finalize_options()' has been
        # called.  'finalize_options()' itself should not pay attention to
        # this flag: it is the business of 'ensure_finalized()', which
        # always calls 'finalize_options()', to respect/update it.
        self.finalized = 0

        for k, v in kw.items():
            setattr(self, k, v)

    user_options = [
        ('additional-test-args=', 'a', "Arguments to pass to underlying test framework"),
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)  # old-style classes
        self.additional_test_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)  # old-style classes
        self.additional_test_args = shlex.split(self.additional_test_args or '')

    def run(self):
        if hasattr(self.distribution, '_egg_fetcher'):
            del self.distribution._egg_fetcher

        if os.path.exists('tox.ini'):
            self.announce('running tox')
            self._run_tox()
        else:
            self.announce('running pytest')
            self._run_pytest()

    def _run_tox(self):
        self.distribution.fetch_build_eggs(self.requirements_tox)

        import tox

        exit_code = tox.cmdline(args=self.additional_test_args)
        raise SystemExit(exit_code)

    def _run_pytest(self):
        self.distribution.fetch_build_eggs(self.requirements_pytest)

        if self.distribution.install_requires:
            self.distribution.fetch_build_eggs(self.distribution.install_requires)

        if self.distribution.tests_require:
            self.distribution.fetch_build_eggs(self.distribution.tests_require)

        self.announce('running "pytest %s"')
        self.with_project_on_sys_path(self._execute_pytest)

    def _execute_pytest(self):
        import pytest

        exit_code = pytest.main(self.additional_test_args)
        raise SystemExit(exit_code)
