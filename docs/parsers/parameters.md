# *module* **parameters**

> [Source: ../../miko/parsers/parameters.py @ line 0](../../miko/parsers/parameters.py#L0)

Parser for the `Parameters` paragraph

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

## *class* parameters.**Parameter**

> [Source: ../../miko/parsers/parameters.py @ line 25-130](../../miko/parsers/parameters.py#L25-L130)

A parameter in the `Parameters` paragraph

### *func* parameters.Parameter.**signature**

> [Source: ../../miko/parsers/parameters.py @ line 28-30](../../miko/parsers/parameters.py#L28-L30)

The signature of the callable, if provided

#### Parameters

- **self**


### *func* parameters.Parameter.**deprecated**

> [Source: ../../miko/parsers/parameters.py @ line 33-35](../../miko/parsers/parameters.py#L33-L35)

If the parameter is considered as deprecated

#### Parameters

- **self**


#### Returns

- bool
    - 

### *func* parameters.Parameter.**signature_parameter**

> [Source: ../../miko/parsers/parameters.py @ line 38-43](../../miko/parsers/parameters.py#L38-L43)

Returns the signature parameter if provided

#### Parameters

- **self**


### *func* parameters.Parameter.**optional**

> [Source: ../../miko/parsers/parameters.py @ line 46-53](../../miko/parsers/parameters.py#L46-L53)

If the parameter is optional

#### Parameters

- **self**


#### Returns

- bool
    - 

### *func* parameters.Parameter.**default**

> [Source: ../../miko/parsers/parameters.py @ line 56-72](../../miko/parsers/parameters.py#L56-L72)

The default value provided for the given parameter

#### Parameters

- **self**


> **Note**
> This can be something other than a string if the `signature` of the callable is provided

### *func* parameters.Parameter.**types**

> [Source: ../../miko/parsers/parameters.py @ line 75-88](../../miko/parsers/parameters.py#L75-L88)

Returns the parameter's possible types

#### Parameters

- **self**


### *func* parameters.Parameter.**render_options**

> [Source: ../../miko/parsers/parameters.py @ line 90-109](../../miko/parsers/parameters.py#L90-L109)

#### Parameters

- **self**


#### Returns

- str
    - 

### *func* parameters.Parameter.**exported**

> [Source: ../../miko/parsers/parameters.py @ line 112-130](../../miko/parsers/parameters.py#L112-L130)

#### Parameters

- **self**


## *class* parameters.**Parameters**

> [Source: ../../miko/parsers/parameters.py @ line 133-166](../../miko/parsers/parameters.py#L133-L166)

Parser for the `Parameters` paragraph

### *const* parameters.Parameters.**element**

> [Source: ../../miko/parsers/parameters.py @ line 135](../../miko/parsers/parameters.py#L135)

### *const* parameters.Parameters.**names**

> [Source: ../../miko/parsers/parameters.py @ line 138](../../miko/parsers/parameters.py#L138)

### *func* parameters.Parameters.**__init__**

> [Source: ../../miko/parsers/parameters.py @ line 141-150](../../miko/parsers/parameters.py#L141-L150)

#### Parameters

- **self**


- **kwargs**


### *func* parameters.Parameters.**signature**

> [Source: ../../miko/parsers/parameters.py @ line 153-155](../../miko/parsers/parameters.py#L153-L155)

The signature of the callable, if provided

#### Parameters

- **self**


### *func* parameters.Parameters.**noself**

> [Source: ../../miko/parsers/parameters.py @ line 158-160](../../miko/parsers/parameters.py#L158-L160)

If the first `self` parameter should be parsed

#### Parameters

- **self**


#### Returns

- bool
    - 

### *func* parameters.Parameters.**__getitem__**

> [Source: ../../miko/parsers/parameters.py @ line 162-163](../../miko/parsers/parameters.py#L162-L163)

#### Parameters

- **self**


- **key**: str


#### Returns

- Parameter
    - 

### *func* parameters.Parameters.**__iter__**

> [Source: ../../miko/parsers/parameters.py @ line 165-166](../../miko/parsers/parameters.py#L165-L166)

#### Parameters

- **self**

