from setuptools import setup, find_packages


setup(name="ncbi-packman",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      version='0.1a',
      entry_points={
          'distutils.setup_keywords': ['packman = packman.core:packman'],
          'setuptools.file_finders': ['packman_extra_files = packman.additional_files:list_files'],
      },
      install_requires=[
          'virtualenv>=12',
          'pbr==0.10.8'
      ],
      zip_safe=False,
)
