#!/usr/bin/env python
import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name='SmashPuttTwitterBox',
    version='0.0.1',
    description="A Twitter Box for Smash Putt",
    license='Python',
    platforms=['POSIX'],
    install_requires=[
        'tweepy',
        'cherrypy',
        'mako'
        # 'pygame',
    ],
    extras_require={
        'RPi': ['RPi.GPIO'],
    },
    author='Andrew Cole',
    author_email='aocole@gmail.com',
    url='https://github.com/aocole/SmashPuttTwitterBox',
    packages=find_packages(),
    scripts=[
        'scripts/smashputttwitterbox',
    ],
    package_data={
        'SmashPuttTwitterBox': ['data/*'],
    },
    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: Python Software Foundation License',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications :: Twitter',
    ],

)
