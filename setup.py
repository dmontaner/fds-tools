#!/usr/local/bin/python3
# setup.py
# 2018-08-15 david.montaner@gmail.com
# fds-tools setup

import os
from setuptools import setup

scripts = [os.path.join('bin', x) for x in os.listdir('bin')]
templates = [x for x in os.listdir('fds_templates') if 'fds-template' in x]

setup(
    name='fds-tools',
    version='0.3.2',
    author='David Montaner',
    author_email='david.montaner@gmail.com',
    license='MIT',
    description='Fast Data Science Tools',
    long_description='''
    Toolkit to improve productivity in small Data Science projects.
    It aims to standardize the processes of creating and executing projects.
    This should help you being quicker and less error prone.
    It may also help when sharing data analysis works making easier to reproduce.
    ''',
    url='https://github.com/dmontaner/fds-tools',
    keywords='analysis productivity reproducibility',
    python_requires='>=2.6',
    install_requires=[
        # 'os',
        # 'sys',
        # 'shutil',
        # 'datetime',
        'argparse',
        'configparser',
        'tabulate',
    ],
    packages=['fds_lib', 'fds_templates'],
    scripts=scripts,
    package_data={'fds_templates': templates}
    # data_files=[('/fds_templates', templates)]
)
