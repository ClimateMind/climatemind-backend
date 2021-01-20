from setuptools import setup, find_packages

setup(
    name="climatemind-backend",
    version="1.0.0",
    description="Climate Mind webapp code",
    author="ClimateMind",
    url="https://github.com/ClimateMind/climatemind-backend",
    py_modules=[
        "config",
    ],
    packages=find_packages(
        exclude=["docs", "tests", ".gitignore", "README.rst", "DESCRIPTION.rst"]
    ),
)
