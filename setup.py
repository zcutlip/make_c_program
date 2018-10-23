from setuptools import setup

setup(name='make_c',
      version='0.1',
      description='A utility to create a simple ' +
      'C source file with a main and open it in an editor.',
      url="TBD",
      packages=['make_c'],
      entry_points={
        'console_scripts': ['make_c=make_c.command_line:main'],
        },
      python_requires='>=3.3'
      )
