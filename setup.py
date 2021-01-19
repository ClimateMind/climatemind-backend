from setuptools import setup, find_packages

setup(name='climatemind-backend',
    version='1.0.0',
    description='Climate Mind webapp code',
    author='ClimateMind',
    url='https://github.com/ClimateMind/climatemind-backend',
    py_modules=["process_new_ontology_and_visualize","process_new_ontology_file","config"],
    packages=find_packages(exclude=["docs","tests", ".gitignore", "README.rst","DESCRIPTION.rst"])
)
