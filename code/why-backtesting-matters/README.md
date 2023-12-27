# Why Backtesting Matters

This folder contains the code used for [this article](https://medium.com/towards-data-science/why-backtesting-matters-and-how-to-do-it-right-731fb9624a).

## Environment

The environment is managed with [Poetry](https://python-poetry.org). To execute the tutorials in the same environment, you can simply run:
```bash
poetry install --no-root
```
To make the virtual environment available as a jupyter kernel, you can run:
```bash
poetry run python -m ipykernel install --user --name=code-collection
```