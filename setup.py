"""
A Tool for the Russian National Corpus
"""
import os
import os.path
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, "trunc", "__about__.py")) as about_file:
    exec(about_file.read(), about)

setup(
    name='trunc',
    version=about['__version__'],
    url=about['__url__'],
    license=about['__license__'],
    author=about['__author__'],
    author_email=about['__author_email__'],
    maintainer=about['__maintainer__'],
    maintainer_email=about['__maintainer_email__'],
    description=about['__description__'],
    long_description=__doc__,
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    entry_points={
        'console_scripts': [
            'trunc = trunc.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    setup_requires=['pytest-runner'],
    tests_requires=['pytest'],
)
