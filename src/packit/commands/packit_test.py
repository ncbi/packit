import os

from setuptools.command.test import test as TestCommand


class PackitTest(TestCommand):
    command_name = 'test'

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

