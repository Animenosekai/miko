# *module* **returns**

> [Source: ../../miko/parsers/returns.py @ line 0](../../miko/parsers/returns.py#L0)

Parser for the `Returns` paragraph

## Imports

- [../../miko/parsers/map.py](../../miko/parsers/map.py): As `MapParser`

## Examples

### Example 1

```python
>>> def func():
...     """
...     Returns
...     -------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
```

## *class* **Returns**

> [Source: ../../miko/parsers/returns.py @ line 23-49](../../miko/parsers/returns.py#L23-L49)

Parser for the `Returns` paragraph

### *attr* Returns.**names**

> [Source: ../../miko/parsers/returns.py @ line 25](../../miko/parsers/returns.py#L25)

### *func* Returns.**signature**

> [Source: ../../miko/parsers/returns.py @ line 42-44](../../miko/parsers/returns.py#L42-L44)

The signature of the callable, if provided

### *func* Returns.**filename**

> [Source: ../../miko/parsers/returns.py @ line 47-49](../../miko/parsers/returns.py#L47-L49)

The filename where the return annotation is defined, if provided
