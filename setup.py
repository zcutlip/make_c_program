from setuptools import setup

about = {}

with open("make_c/__about__.py") as fp:
    exec(fp.read(), about)

with open("README.md", "r") as fp:
    long_description = fp.read()

setup(name=about["__title__"],
      version=about["__version__"],
      description=about["__summary__"],
      long_description=long_description,
      long_description_content_type="text/markdown",
      author="Zachary Cutlip",
      author_email="uid000@gmail.com",
      license="MIT",
      url="https://github.com/zcutlip/make_c_program",
      packages=['make_c'],
      entry_points={
          'console_scripts': ['make_c=make_c.command_line:main'],
},
    python_requires='>=3.3'
)
