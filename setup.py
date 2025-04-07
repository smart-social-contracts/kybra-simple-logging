from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="kybra_simple_logging",
    version="0.1.3",
    author="Smart Social Contracts",
    author_email="smartsocialcontracts@gmail.com",
    description="A robust logging system for Internet Computer canisters built with Kybra",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/smart-social-contracts/kybra_simple_logging",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
    install_requires=[],
)
