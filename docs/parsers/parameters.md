# *module* **parameters**

> [Source: ../../miko/parsers/parameters.py @ line 0](../../miko/parsers/parameters.py#L0)

Parser for the `Parameters` paragraph

## Imports

- [../../miko/parsers/map.py](../../miko/parsers/map.py): As `MapElement`

## Examples

### Example 1

```python
>>> def func():
...     """
...     Parameters
...     ----------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
```

## *class* **Parameter**

> [Source: ../../miko/parsers/parameters.py @ line 25-130](../../miko/parsers/parameters.py#L25-L130)

A parameter in the `Parameters` paragraph

### *func* Parameter.**signature**

> [Source: ../../miko/parsers/parameters.py @ line 28-30](../../miko/parsers/parameters.py#L28-L30)

The signature of the callable, if provided

### *func* Parameter.**deprecated**

> [Source: ../../miko/parsers/parameters.py @ line 33-35](../../miko/parsers/parameters.py#L33-L35)

If the parameter is considered as deprecated

#### Returns

- `bool`

### *func* Parameter.**signature_parameter**

> [Source: ../../miko/parsers/parameters.py @ line 38-43](../../miko/parsers/parameters.py#L38-L43)

Returns the signature parameter if provided

### *func* Parameter.**optional**

> [Source: ../../miko/parsers/parameters.py @ line 46-53](../../miko/parsers/parameters.py#L46-L53)

If the parameter is optional

#### Returns

- `bool`

### *func* Parameter.**default**

> [Source: ../../miko/parsers/parameters.py @ line 56-72](../../miko/parsers/parameters.py#L56-L72)

The default value provided for the given parameter

> **Note**
> This can be something other than a string if the `signature` of the callable is provided

### *func* Parameter.**types**

> [Source: ../../miko/parsers/parameters.py @ line 75-88](../../miko/parsers/parameters.py#L75-L88)

Returns the parameter's possible types

### *func* Parameter.**render_options**

> [Source: ../../miko/parsers/parameters.py @ line 90-109](../../miko/parsers/parameters.py#L90-L109)

#### Returns

- `str`

### *func* Parameter.**exported**

> [Source: ../../miko/parsers/parameters.py @ line 112-130](../../miko/parsers/parameters.py#L112-L130)

## *class* **Parameters**

> [Source: ../../miko/parsers/parameters.py @ line 133-166](../../miko/parsers/parameters.py#L133-L166)

Parser for the `Parameters` paragraph

### *attr* Parameters.**element**

> [Source: ../../miko/parsers/parameters.py @ line 135](../../miko/parsers/parameters.py#L135)

### *attr* Parameters.**names**

> [Source: ../../miko/parsers/parameters.py @ line 138](../../miko/parsers/parameters.py#L138)

### *func* Parameters.**signature**

> [Source: ../../miko/parsers/parameters.py @ line 153-155](../../miko/parsers/parameters.py#L153-L155)

The signature of the callable, if provided

### *func* Parameters.**noself**

> [Source: ../../miko/parsers/parameters.py @ line 158-160](../../miko/parsers/parameters.py#L158-L160)

If the first `self` parameter should be parsed

#### Returns

- `bool`
