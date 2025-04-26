from setuptools import find_packages, setup
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# CLI documentation is now included in the main README.md

setup(
    name="kybra_simple_logging",
    version="0.1.4",  # Increment version for new CLI feature
    author="Smart Social Contracts",
    author_email="smartsocialcontracts@gmail.com",
    description="A robust logging system for Internet Computer canisters built with Kybra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smart-social-contracts/kybra-simple-logging",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ksl=kybra_simple_logging.cli:main",  # Register the CLI command with new name
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
