import re
import sys
from codecs import open  # To use a consistent encoding
from os import path

from setuptools import setup  # Always prefer setuptools over distutils


def strip(line):
    """Strip comments and whitespace from a line of text."""
    return line.split('#', 1)[0].strip()


def requirements_from_file(filename):
    """Parses a pip requirements file into a list."""
    with open(filename, 'r') as fd:
        return [strip(line) for line in fd if strip(line)]


def read(fname, URL, URLImage):
    """Read the content of a file."""
    with open(path.join(path.dirname(__file__), fname)) as fd:
        readme = fd.read()
    if hasattr(readme, 'decode'):
        # In Python 3, turn bytes into str.
        readme = readme.decode('utf8')
    # turn relative links into absolute ones
    readme = re.sub(r'`<([^>]*)>`__',
                    r'`\1 <' + URL + r"/blob/main/\1>`__",
                    readme)
    readme = re.sub(r"\.\. image:: /", ".. image:: " + URLImage + "/", readme)

    return readme


here = path.abspath(path.dirname(__file__))

about = {}
with open(path.join(here, 'mechanicalsoup', '__version__.py'),
          'r', 'utf-8') as fd:
    exec(fd.read(), about)

# Don't install pytest-runner on every setup.py run, just for tests.
# See https://pypi.org/project/pytest-runner/#conditional-requirement
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

setup(
    name=about['__title__'],

    # useful: python setup.py sdist bdist_wheel upload
    version=about['__version__'],

    description=about['__description__'],
    long_description=read('README.rst', about['__github_url__'], about[
        '__github_assets_absoluteURL__']),
    url=about['__url__'],
    project_urls={
        'Source': about['__github_url__'],
    },

    license=about['__license__'],

    python_requires='>=3.9',

    classifiers=[
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=['mechanicalsoup'],

    # List run-time dependencies here. These will be installed by pip
    # when your project is installed. For an analysis of
    # "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=requirements_from_file('requirements.txt'),
    setup_requires=pytest_runner,
    tests_require=requirements_from_file('tests/requirements.txt'),
)
