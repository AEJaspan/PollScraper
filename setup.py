#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'pytest', 'beautifulsoup4', 'numpy', 'pandas', 'requests', 'urllib3', 'urlpath']

test_requirements = [ ]

setup(
    author="Adam Jaspan",
    author_email='adam.jaspan@googlemail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A production-ready web scraping utility, built to monitor polling data hosted by the Economist data team.",
    entry_points={
        'console_scripts': [
            'pollscraper=pollscraper.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pollscraper',
    name='pollscraper',
    packages=find_packages(include=['pollscraper', 'pollscraper.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/AEJaspan/pollscraper',
    version='0.1.0',
    zip_safe=False,
)
