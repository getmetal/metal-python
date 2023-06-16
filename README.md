# 🤘 Metal Python SDK

- [**Developer Documentation**](https://docs.getmetal.io/sdk-python)
- [**PyPi Package**](https://pypi.org/project/metal-sdk/)

## Setup

```bash
$ pip3 install metal-sdk
```

## Usage

```python
from metal_sdk.metal import Metal


metal = Metal("api_key", "client_id", "index_id");

metal.index({ "text": "a" })
metal.index({ "text": "b" })
metal.index({ "text": "c" })
```

[Async example](./examples/example_async.py)

## Testing

```bash
$ python3 -m unittest tests/test_metal.py
```

[Reference](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
