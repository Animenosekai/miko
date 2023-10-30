# *module* **flag**

> [Source: ../../miko/parsers/flag.py @ line 0](../../miko/parsers/flag.py#L0)

Defines the flag parsers base class  
A flag is what describes a boolean value in a docstring  
If the flag is present, it will be set to True, otherwise it will be set to False

## Imports

- [../../miko/parsers/parser.py](../../miko/parsers/parser.py): As `Parser`

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

## *class* **FlagParser**

> [Source: ../../miko/parsers/flag.py @ line 25-49](../../miko/parsers/flag.py#L25-L49)

A flag parser

### *attr* FlagParser.**element**

> **Important**
> This attr is of type `None`

> [Source: ../../miko/parsers/flag.py @ line 27](../../miko/parsers/flag.py#L27)

### *attr* FlagParser.**elements**

> **Important**
> This attr is of type `None`

> [Source: ../../miko/parsers/flag.py @ line 28](../../miko/parsers/flag.py#L28)

### *func* FlagParser.**set_flag**

> [Source: ../../miko/parsers/flag.py @ line 30-32](../../miko/parsers/flag.py#L30-L32)

Sets the flag

### *func* FlagParser.**dumps**

> [Source: ../../miko/parsers/flag.py @ line 34-37](../../miko/parsers/flag.py#L34-L37)

#### Parameters

- **indent**: `int`
  - Default Value: `4`


- **prefix**: `str`
  - Default Value: `!`


### *func* FlagParser.**flag**

> [Source: ../../miko/parsers/flag.py @ line 40-41](../../miko/parsers/flag.py#L40-L41)

### *func* FlagParser.**exported**

> [Source: ../../miko/parsers/flag.py @ line 44-46](../../miko/parsers/flag.py#L44-L46)

The exported data
