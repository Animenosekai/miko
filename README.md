# `zero`

<img src="./docs/zero_syo.svg" alt="zero" align="right" height="220px">

 A new Python documentation style

***See how to use a Python object at a glance!***

<br>
<br>

[![PyPI version](https://badge.fury.io/py/zero.svg)](https://pypi.org/project/zero/)
[![Downloads](https://static.pepy.tech/personalized-badge/zero?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Total%20Downloads)](https://pepy.tech/project/zero)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/zero)](https://pypistats.org/packages/zero)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/zero)](https://pypi.org/project/zero/)
[![PyPI - Status](https://img.shields.io/pypi/status/zero)](https://pypi.org/project/zero/)
[![GitHub - License](https://img.shields.io/github/license/Animenosekai/zero)](https://github.com/Animenosekai/zero/blob/master/LICENSE)
[![GitHub top language](https://img.shields.io/github/languages/top/Animenosekai/zero)](https://github.com/Animenosekai/zero)
[![CodeQL Checks Badge](https://github.com/Animenosekai/zero/workflows/CodeQL%20Python%20Analysis/badge.svg)](https://github.com/Animenosekai/zero/actions?query=workflow%3ACodeQL)
[![Pytest](https://github.com/Animenosekai/zero/actions/workflows/pytest.yml/badge.svg)](https://github.com/Animenosekai/zero/actions/workflows/pytest.yml)
![Code Size](https://img.shields.io/github/languages/code-size/Animenosekai/zero)
![Repo Size](https://img.shields.io/github/repo-size/Animenosekai/zero)
![Issues](https://img.shields.io/github/issues/Animenosekai/zero)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

#### Python

You will need Python 3 to use this module

```bash
# vermin output
Minimum required versions: 3.0
Incompatible versions:     2
```

## Installing

### Option 1: From PyPI

```bash
pip install --upgrade zero
```

### Option 2: From Git

```bash
pip install --upgrade git+https://github.com/Animenosekai/zero
```

You can check if you successfully installed it by printing out its version:

```bash
$ python -c "import zero; print(zero.__version__)"
# output:
zero v1.0
```

## Purpose

This new style aims at bringing an ease of use for both humans and computers.

It also helps me get concise while writing docstrings as I tend to use different styles even within a same file.

## Style

Zero defines a new way of documenting your source code.

You will here learn the different sections of your documentation string.

### Outline

The *Zero* way of documenting stuff is by using Markdown in your documentation and following the rules below.

#### Start

When you want to document the object, you need to start the docstring with 3 quotation marks, preferably double quotation marks.

You also need to add a line break and pad the whole documentation to line up with the start of the object name.

> Example: we are using 3 double quotation marks, and we start where the object name starts after a line break.

```python
def func():
    """
    It needs to start here

    Here we continue the documentation string
^^^^
(do not use this space)
    """
    pass
```

#### End

The documentation string ends when 3 quotation marks (the same as the beginning ones) are added after the padding.

### Description

After starting the documentation string, you can add a description for your object as a normal string.

There is not much styling or rules to follow since all the content outside any section is considered part of the description.

> Example: We are giving a description of the function at the start, but also at the end.

```python
def func():
    """
    Hello, this is a description.

    Returns
    ----------
    bool
        The result of the function.

    But this is also part of the description.
    """
```

### Parameters

You can define what are the different parameters/arguments the callable object is taking.

To start explaining the different parameters, you need to use the `Parameters` section name, followed by a line-break and at least 3 hyphens.

A single parameter element is defined by a name, followed by some options. And, on a new line, with a left padding, its description.

> Example

```python
def func(a, b: int, c = ""):
    """
    Parameters
    ----------
    a: bool
        this is the first argument
    b: int | float, default = 1.2
        this is the second argument
    c: str, optional
        this is the third argument
        it can have multiple lines
    """
```

#### The options

You can specify options for each parameter.

The options are separated from the parameter name using a colon and a space.

Each option is separated by a comma.

- `<type>` : defines the type of the parameter.
- `optional` : defines a parameter as being optional, without needing to specify its default value. *(useful for example with keyword arguments)*
- `default` : defines a parameter as being optional, by giving it a default value.

##### Types

Types can be defined by giving the element class name or *dot notation* path.

> Example: `str`, `translatepy.language.Language`

You can specify multiple types using the vertical bar separator.

> Example: `int | float`

##### Default

You can define a default value using an equal sign.

> Example: `a = 1`, `b=True`

### Returned Value

### Example

### Warnings

### Exceptions

### Notes

### Change log

### Deprecation Notice

### Copyright

## Usage

*Here, there will be the Python API Reference.*

## Deployment

This module is currently in development and might contain bugs.

Feel free to use it in production if you feel like it is suitable for your production even if you may encounter issues.

## Contributing

Pull requests are welcome. For major changes, please open a discussion first to discuss what you would like to change.

Please make sure to update the tests as appropriate.

## Built With

- [something](https://something.com) - to do something

## Authors

- **Anime no Sekai** - *Initial work* - [Animenosekai](https://github.com/Animenosekai)

## Acknowledgments

...

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
