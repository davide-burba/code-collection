# Local vs Global Forecasting

This folder contains the code used for [this article](https://medium.com/towards-data-science/local-vs-global-forecasting-what-you-need-to-know-1cc29e66cae0).

## Environment

The environment is managed with [Poetry](https://python-poetry.org). To execute the tutorials in the same environment, you can simply run:
```bash
poetry install --no-root
```
To make the virtual environment available as a jupyter kernel, you can run:
```bash
poetry run python -m ipykernel install --user --name=code-collection
```