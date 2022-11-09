# Code style

The Python code style is formatted using [Black](https://pypi.org/project/black/). Black is a file formatter that converts your code to follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) standards. PEP 8 provides guidelines and best practices for writing Python, and is the standard style used for modern Python libraries.

Open the terminal/command line and install Black by running `pip install black`. Note: Python 3.6.0+ is required.

1. Use the terminal/command-line to navigate to the climatemind-backend directory
2. Run Black locally to see which files need formatting using `python3 -m black --check ./`
3. Use Black to automatically format your files using `python3 -m black ./`
