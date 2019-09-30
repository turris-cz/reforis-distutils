#!/usr/bin/env python

from setuptools import setup

setup(
    name="reforis_distutils",
    version="0.0.1",
    description="Distutils patches to add commands for reForis handling",
    author="CZ.NIC, z. s. p. o.",
    url="https://gitlab.labs.nic.cz/turris/reforis/reforis-distutils",
    license="GPL-3.0",
    requires=[],
    install_requires=["babel"],
    provides=["reforis_distutils"],
    packages=["reforis_distutils"],
)
