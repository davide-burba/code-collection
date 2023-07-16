# Code Collection

This repository contains the collection of code examples used for [my blog articles](https://medium.com/@davide.burba).


## Environment

I use [Poetry](https://python-poetry.org) to manage dependencies. To execute the tutorials in the same environment, you can simply run:
```bash
poetry install --no-root
```
To make the virtual environment available as a jupyter kernel, you can run:
```bash
poetry run python -m ipykernel install --user --name=code-collection
```

Some examples need different environments to be run. For these, there are specific instructions in the README inside the example folder.
