import os
import sys
import logging
import warnings
from distutils import errors

from setuptools import dist
from setuptools.command.easy_install import easy_install

from pip.commands.install import InstallCommand as PipInstallCommand

from pbr import util
from pbr import hooks, pbr_json
from pbr.core import _monkeypatch_distribution, _restore_distribution_monkeypatch, string_type, integer_types

from .hooks import setup_hook


def pbr(distribution, attr, value):
    """Implements the actual pbr setup() keyword.  When used, this should be
    the only keyword in your setup() aside from `setup_requires`.

    If given as a string, the value of pbr is assumed to be the relative path
    to the setup.cfg file to use.  Otherwise, if it evaluates to true, it
    simply assumes that pbr should be used, and the default 'setup.cfg' is
    used.

    This works by reading the setup.cfg file, parsing out the supported
    metadata and command options, and using them to rebuild the
    `DistributionMetadata` object and set the newly added command options.

    The reason for doing things this way is that a custom `Distribution` class
    will not play nicely with setup_requires; however, this implementation may
    not work well with distributions that do use a `Distribution` subclass.
    """

    try:
        _monkeypatch_distribution()
        if not value:
            return
        if isinstance(value, string_type):
            path = os.path.abspath(value)
        else:
            path = os.path.abspath('setup.cfg')
        if not os.path.exists(path):
            raise errors.DistutilsFileError(
                'The setup.cfg file %s does not exist.' % path)

        # Converts the setup.cfg file to setup() arguments
        try:
            attrs = util.cfg_to_args(path)
        except Exception:
            e = sys.exc_info()[1]
            # NB: This will output to the console if no explicit logging has
            # been setup - but thats fine, this is a fatal distutils error, so
            # being pretty isn't the #1 goal.. being diagnosable is.
            logging.exception('Error parsing')
            raise errors.DistutilsSetupError(
                'Error parsing %s: %s: %s' % (path, e.__class__.__name__, e))

        # Repeat some of the Distribution initialization code with the newly
        # provided attrs
        if attrs:
            # Skips 'options' and 'licence' support which are rarely used; may
            # add back in later if demanded
            for key, val in attrs.items():
                if hasattr(distribution.metadata, 'set_' + key):
                    getattr(distribution.metadata, 'set_' + key)(val)
                elif hasattr(distribution.metadata, key):
                    setattr(distribution.metadata, key, val)
                elif hasattr(distribution, key):
                    setattr(distribution, key, val)
                else:
                    msg = 'Unknown distribution option: %s' % repr(key)
                    warnings.warn(msg)

        # Re-finalize the underlying Distribution
        # FIXME: We need to copy the whole function from PBR in order to modify the following line
        dist._get_unpatched(distribution.__class__).finalize_options(distribution)

        # This bit comes out of distribute/setuptools
        if isinstance(distribution.metadata.version, integer_types + (float,)):
            # Some people apparently take "version number" too literally :)
            distribution.metadata.version = str(distribution.metadata.version)

        # This bit of hackery is necessary so that the Distribution will ignore
        # normally unsupport command options (namely pre-hooks and post-hooks).
        # dist.command_options is normally a dict mapping command names to
        # dicts of their options.  Now it will be a defaultdict that returns
        # IgnoreDicts for the each command's options so we can pass through the
        # unsupported options
        ignore = ['pre_hook.*', 'post_hook.*']
        distribution.command_options = util.DefaultGetDict(lambda: util.IgnoreDict(ignore))
    finally:
        _restore_distribution_monkeypatch()


def patch_pbr():
    hooks.setup_hook = setup_hook
    # Disabling annoying pbr.json
    pbr_json.write_pbr_json = lambda *a, **k: None


def patch_setuptools(fetch_directives=('index_url', 'find_links')):

    orig = easy_install.finalize_options

    def patched_finalize_options(self):
        cmd = PipInstallCommand()
        config = cmd.parser.parse_args([])[0]
        for option in fetch_directives:
            try:
                value = getattr(config, option)
            except AttributeError:
                continue
            setattr(self, option, value)
        orig(self)

    easy_install.finalize_options = patched_finalize_options


def patch(config=None):
    patch_pbr()
    patch_setuptools()


def packit(dist, attr, value):
    if not value:
        return

    patch()
    pbr(dist, attr, value)
