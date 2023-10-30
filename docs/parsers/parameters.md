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

> [Source: ../../miko/parsers/parameters.py @ line 25-134](../../miko/parsers/parameters.py#L25-L134)

A parameter in the `Parameters` paragraph

### *func* Parameter.**signature**

> [Source: ../../miko/parsers/parameters.py @ line 28-30](../../miko/parsers/parameters.py#L28-L30)

The signature of the callable, if provided

#### Returns

- `Optional`

### *func* Parameter.**filename**

> [Source: ../../miko/parsers/parameters.py @ line 33-35](../../miko/parsers/parameters.py#L33-L35)

The filename where the parameter is defined, if provided

#### Returns

- `Optional`

### *func* Parameter.**deprecated**

> [Source: ../../miko/parsers/parameters.py @ line 38-40](../../miko/parsers/parameters.py#L38-L40)

If the parameter is considered as deprecated

#### Returns

- `bool`

### *func* Parameter.**signature_parameter**

> [Source: ../../miko/parsers/parameters.py @ line 43-48](../../miko/parsers/parameters.py#L43-L48)

Returns the signature parameter if provided

#### Returns

- `Optional`

### *func* Parameter.**optional**

> [Source: ../../miko/parsers/parameters.py @ line 51-58](../../miko/parsers/parameters.py#L51-L58)

If the parameter is optional

#### Returns

- `bool`

### *func* Parameter.**default**

> [Source: ../../miko/parsers/parameters.py @ line 61-77](../../miko/parsers/parameters.py#L61-L77)

The default value provided for the given parameter

#### Returns

- `Union`

> **Note**
> This can be something other than a string if the `signature` of the callable is provided

### *func* Parameter.**types**

> [Source: ../../miko/parsers/parameters.py @ line 80-95](../../miko/parsers/parameters.py#L80-L95)

Returns the parameter's possible types

#### Returns

- `set`

### *func* Parameter.**render_options**

> [Source: ../../miko/parsers/parameters.py @ line 97-114](../../miko/parsers/parameters.py#L97-L114)

#### Returns

- `str`

### *func* Parameter.**exported**

> [Source: ../../miko/parsers/parameters.py @ line 117-134](../../miko/parsers/parameters.py#L117-L134)

## *class* **Parameters**

> [Source: ../../miko/parsers/parameters.py @ line 137-189](../../miko/parsers/parameters.py#L137-L189)

Parser for the `Parameters` paragraph

### *attr* Parameters.**element**

> [Source: ../../miko/parsers/parameters.py @ line 139](../../miko/parsers/parameters.py#L139)

### *attr* Parameters.**names**

> [Source: ../../miko/parsers/parameters.py @ line 142](../../miko/parsers/parameters.py#L142)

### *func* Parameters.**signature**

> [Source: ../../miko/parsers/parameters.py @ line 176-178](../../miko/parsers/parameters.py#L176-L178)

The signature of the callable, if provided

#### Returns

- `Optional`

### *func* Parameters.**noself**

> [Source: ../../miko/parsers/parameters.py @ line 181-183](../../miko/parsers/parameters.py#L181-L183)

If the first `self` parameter should be parsed

#### Returns

- `bool`
