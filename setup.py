# Copyright (c) 2022 Javier Escalada Gómez
# All rights reserved.

from setuptools import setup, find_packages
from pathlib import Path
from custom_json_encoder import __version__

base = Path(__file__).parent
long_description = (base / "README.md").read_text()

setup(
    name='custom_json_encoder',
    version=__version__,
    url='https://github.com/Kerrigan29a/py_custom_json_encoder.git',
    author='Javier Escalada Gómez',
    author_email='kerrigan29a@gmail.com',
    description='A JSON encoder that allows customizing the indentation based on the content and the width of the line.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),    
    install_requires=[],
    license='BSD 3-Clause Clear License',
    entry_points={
        'console_scripts': [
            'custom_json_encoder=custom_json_encoder.__main__:main',
        ],
    },
    # From https://pypi.org/classifiers/    
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Utilities',
          ],
    platforms=['any'],
    keywords=['json', 'encoder', 'pretty-print', 'width'],
)
