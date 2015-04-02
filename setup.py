from setuptools import setup, find_packages


setup(name="ncbi-packman",
      packages=find_packages(),
      namespace_packages=['packman'],
      version='0.1a',
      entry_points={
          'distutils.setup_keywords': ['packman = packman.core:packman'],
          'setuptools.file_finders': ['packman_extra_files = packman_extra.additional_files:list_files'],
      },
      install_requires=['pbr'],
      zip_safe=False,
)
