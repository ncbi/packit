import os

from setuptools.command.test import test as TestCommand


class PackitTest(TestCommand):
    command_name = 'test'

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
        ('tox-args=', 't', "Arguments to pass to tox"),
        ('pytest-args=', 'p', "Arguments to pass to py.test")
    ]

    def initialize_options(self):
        TestCommand.initialize_options(self)  # old-style classes
        self.tox_args = None
        self.pytest_args = None

    def finalize_options(self):
        TestCommand.finalize_options(self)  # old-style classes
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        if os.path.exists('tox.ini'):
            self._run_tox()
        else:
            self._run_pytest()

    def _run_tox(self):
        import tox

        errno = tox.cmdline(args=self.tox_args)
        raise SystemExit(errno)

    def _run_pytest(self):
        import pytest
        pytest.main(self.pytest_args)

