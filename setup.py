import setuptools
from aionet import __version__, __author__

with open("README.rst", "r") as fh:
  long_description = fh.read()

setuptools.setup(
  name="aionet",
  version=__version__,
  author=__author__,
  author_email="aaqrabaw@gmail.com",
  description="async networking SDK",
  long_description=long_description,
  url="https://github.com/Ali-aqrabawi/aionet",
  packages=setuptools.find_packages(),
  include_package_data=True,
  install_requires=['asyncssh', 'textfsm'],
  classifiers=[
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
)
