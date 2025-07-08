# pyfwimagebuilder - Firmware Image Builder
This utility is used to produce image files which can be used with the pymdfu tool: https://pypi.org/project/pymdfu/

![PyPI - Format](https://img.shields.io/pypi/format/pyfwimagebuilder)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pyfwimagebuilder)
![PyPI - License](https://img.shields.io/pypi/l/pyfwimagebuilder)

## Overview

* install using pip from pypi: https://pypi.org/project/pyfwimagebuilder

## Usage
pyfwimagebuilder can be used as a command-line interface or a library

### Building an image from the command-line
for help, use:
```bash
pyfwimagebuilder --help
```

Example usage:

Building an image:
```bash
pyfwimagebuilder build -i myapp.hex -c myconfig.toml -o myimage.img
```

Decoding an image:
```bash
pyfwimagebuilder decode -i myapp.img -c myconfig.toml -o myimage.txt
```

### Additional command-line switches
* -v LEVEL for selecting logging verbosity ('debug', 'info', 'warning', 'error', 'critical')