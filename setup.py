from setuptools import setup, find_packages
with open("requirements.txt") as requirements_file:
    install_requirements = requirements_file.read().splitlines()

setup(
    name = "pyvoicevox",
    version = "0.0.1",
    description = "A simple python binding for VOICEVOX engine.",
    author = "Ryo Nakamura",
    author_email = "upa@haeena.net",
    packages = find_packages(),
    install_requires = install_requirements,
    classifiers = [
        "Programming Language :: Python :: 3",
    ]
)
