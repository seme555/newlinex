# Tests

Schema unit tests cover the Pydantic models in `src/models/schemas.py` (sales, products, customers).

## Run locally

```bash
pip install -r tests/requirements.txt
PYTHONPATH=. pytest tests/ -v
```

## CI

GitHub Actions runs the same suite on Python 3.10 and 3.11 for every push and pull request to `main`.
