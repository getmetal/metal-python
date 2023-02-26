# 🤘 Metal Python SDK

[**Developer Documentation**](https://docs.getmetal.io/sdk-python)
[**PyPi Package**](https://pypi.org/project/metal-sdk/)

## Setup

```bash
pip install metal-sdk
```

## Usage

```python
  metal = MetalSDK("api_key", "client_id", "app_id");
  meta.index({ text: 'a' })
  meta.index({ text: 'b' })
  meta.index({ text: 'c' })
```

## Contributing

```bash
$ python3 -m build
$ python3 -m twine upload dist/*
```

[Reference](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
