# -*- coding: utf-8 -*-

import os

from setuptools import setup, find_packages

BASE_DIR = os.path.realpath(os.path.dirname(__file__))


def parse_requirements():
    """
    @summary: 获取依赖
    """
    requirements = []
    if os.path.isfile(os.path.join(BASE_DIR, "requirements.txt")):
        with open(os.path.join(BASE_DIR, "requirements.txt"), 'r') as reqs_file:
            for line in reqs_file.readlines():
                line = line.strip()
                if line:
                    requirements.append(line)
    return requirements



if __name__ == "__main__":
    setup(
        version="1.0.1",
        name="python_atom_sdk",
        description="",
        cmdclass={},
        packages=find_packages(),
        package_data={'': ['*.txt', '*.TXT']},
        install_requires=parse_requirements(),

        author="bk-ci",
        license="Copyright(c)2010-2019 landun All Rights Reserved."
    )
