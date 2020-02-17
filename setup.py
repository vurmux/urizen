#!/usr/bin/python3

from setuptools import setup, find_packages


setup(
    name='urizen',
    version='0.0.2',
    description='Roguelike dungeon generation library',
    long_description='',
    url='https://github.com/vurmux/urizen',
    author='Andrey Voronov',
    author_email='vurmux@gmail.com',
    license='Apache',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='',
    packages=find_packages(exclude=['doc', 'res']),
    install_requires=[
        'noise',
        'colorama',
        'Pillow'
    ],
    extras_require={
        'dev': [],
        'test': ['coverage'],
    },
    package_data={},
    entry_points={},
)

