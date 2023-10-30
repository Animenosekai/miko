# *module* **returns**

> [Source: ../../miko/parsers/returns.py @ line 0](../../miko/parsers/returns.py#L0)

Parser for the `Returns` paragraph

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

> [Source: ../../miko/parsers/returns.py @ line 23-45](../../miko/parsers/returns.py#L23-L45)

Parser for the `Returns` paragraph

### *const* Returns.**names**

> [Source: ../../miko/parsers/returns.py @ line 25](../../miko/parsers/returns.py#L25)

### *func* Returns.**__init__**

> [Source: ../../miko/parsers/returns.py @ line 27-39](../../miko/parsers/returns.py#L27-L39)

#### Parameters

- **kwargs**


### *func* Returns.**signature**

> [Source: ../../miko/parsers/returns.py @ line 43-45](../../miko/parsers/returns.py#L43-L45)

The signature of the callable, if provided
