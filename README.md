
---
# Sipefield's pylab

[![codecov](https://codecov.io/gh/Gronemeyer/PyLab/branch/main/graph/badge.svg?token=PyLab_token_here)](https://codecov.io/gh/Gronemeyer/PyLab)
[![CI](https://github.com/Gronemeyer/PyLab/actions/workflows/main.yml/badge.svg)](https://github.com/Gronemeyer/PyLab/actions/workflows/main.yml)

Awesome pylab created by Gronemeyer

## Install it from PyPI

```bash
pip install pylab
```

## Usage

```py
from pylab import BaseClass
from pylab import base_function

BaseClass().base_method()
base_function()
```

```bash
$ python -m pylab
#or
$ pylab
```

## Adding a configuration file to a mmc.core() object

```py
MM_CONFIG = r'C:/dev/micro-manager_configuration.cfg'

# Initialize the Core
mmc = CMMCorePlus().instance()
mmc.loadSystemConfiguration(MM_CONFIG)
```


Read the [CONTRIBUTING.md](CONTRIBUTING.md) file.
