# Telugu Typesetting for the Bhagavad Gita

This repository contains resources to produce a LaTeX-typeset PDF for the Bhagavad Gita. Here, the written form matches the pronounciation for chanting the Bhagavad Gita (see the [SGS Gita Foundation](https://www.sgsgitafoundation.org/assets/resources/SrimadBhagawadGeeta_English.pdf) PDF as reference).

## Setup

Note: we are using [Poetry](https://python-poetry.org/) as the build system for the Python program to generate the LaTeX files. You should have `poetry` installed on your system.

```bash
poetry install
```

## Generating LaTeX Files

```bash
poetry run typesetting
```
