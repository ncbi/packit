from setuptools import setup, find_packages


setup(name="packit",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      version='0.1a',
      entry_points={
          'distutils.setup_keywords': ['packit = packit.core:packit'],
          'setuptools.file_finders': ['packit_extra_files = packit.additional_files:list_files'],
      },
      install_requires=[
          'virtualenv>=12',
          'pbr==0.10.8'
      ],
      zip_safe=False,
      license='NCBI license',
)
