from setuptools import setup

import os

# For this test, we will use our own "git" that's just a script.
os.putenv('PATH', '.:' + os.getenv('PATH'))

setup(
    setup_requires=['packit'],
    packit=True)
