from setuptools import setup, find_packages


setup(name="ncbi-packman",
      packages=find_packages(),
      version='0.1a',
      entry_points={
          'distutils.setup_keywords': ['packman = packman.core:packman']
      },
      install_requires=['pbr'],
)
