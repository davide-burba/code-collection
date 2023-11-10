# Scraping with GPT and Google Search

This project showcases a minimal example on how to perform automated web scraping with [GPT](https://platform.openai.com/docs/guides/gpt/gpt-models) and the [googlesearch-python](https://pypi.org/project/googlesearch-python/) package.

The related article is coming soon.

## Environment

The environment is managed with [Poetry](https://python-poetry.org). To execute the tutorials in the same environment, you can simply run:
```bash
poetry install --no-root
```
To make the virtual environment available as a jupyter kernel, you can run:
```bash
poetry run python -m ipykernel install --user --name=scraping-gpt-googlesearch
```