from setuptools import find_packages, setup
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kybra_simple_logging",
    version="0.2.0",
    author="Smart Social Contracts",
    author_email="smartsocialcontracts@gmail.com",
    description="A robust logging system for Internet Computer canisters built with Kybra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smart-social-contracts/kybra-simple-logging",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "kslog=kybra_simple_logging.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Debuggers",
    ],
    python_requires=">=3.7",
    install_requires=[],
)
