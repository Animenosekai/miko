# *module* **flag**

> [Source: ../../miko/parsers/flag.py @ line 0](../../miko/parsers/flag.py#L0)

Defines the flag parsers base class  
A flag is what describes a boolean value in a docstring  
If the flag is present, it will be set to True, otherwise it will be set to False

## Examples

### Example 1

```python
>>> def func():
...     """
...     This is a function
...
...     ! FLAG
...     ! YOU'RE COOL
...     
...     (description)
...     """
```

## *class* flag.**FlagParser**

> [Source: ../../miko/parsers/flag.py @ line 25-49](../../miko/parsers/flag.py#L25-L49)

A flag parser

### *const* flag.FlagParser.**element**

> [Source: ../../miko/parsers/flag.py @ line 27](../../miko/parsers/flag.py#L27)

### *const* flag.FlagParser.**elements**

> [Source: ../../miko/parsers/flag.py @ line 28](../../miko/parsers/flag.py#L28)

### *func* flag.FlagParser.**set_flag**

> [Source: ../../miko/parsers/flag.py @ line 30-32](../../miko/parsers/flag.py#L30-L32)

Sets the flag

#### Parameters

- **self**


### *func* flag.FlagParser.**dumps**

> [Source: ../../miko/parsers/flag.py @ line 34-37](../../miko/parsers/flag.py#L34-L37)

#### Parameters

- **self**


- **indent**: int
  - Default Value: `4`


- **prefix**: str
  - Default Value: `!`


### *func* flag.FlagParser.**flag**

> [Source: ../../miko/parsers/flag.py @ line 40-41](../../miko/parsers/flag.py#L40-L41)

#### Parameters

- **self**


### *func* flag.FlagParser.**exported**

> [Source: ../../miko/parsers/flag.py @ line 44-46](../../miko/parsers/flag.py#L44-L46)

The exported data

#### Parameters

- **self**


### *func* flag.FlagParser.**__repr__**

> [Source: ../../miko/parsers/flag.py @ line 48-49](../../miko/parsers/flag.py#L48-L49)

#### Parameters

- **self**


#### Returns

- str
    - 