# ESGVOC BACKEND

Earth Science - VOCabulary backend

## How to contribute

### Install Python dev environment

* Pip

```bash
pip install -e .
```

* Rye

```bash
rye sync
```

### Linters & code formatters

* Pip

```bash
pip install pre-commit
pre-commit install
```

* Rye

```bash
rye install
rye run pre-commit install
```

### Start API server

* Rye

```bash
rye run server
```
