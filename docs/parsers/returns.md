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

## *class* returns.**Returns**

> [Source: ../../miko/parsers/returns.py @ line 23-44](../../miko/parsers/returns.py#L23-L44)

Parser for the `Returns` paragraph

### *const* returns.Returns.**names**

> [Source: ../../miko/parsers/returns.py @ line 25](../../miko/parsers/returns.py#L25)

### *func* returns.Returns.**__init__**

> [Source: ../../miko/parsers/returns.py @ line 27-39](../../miko/parsers/returns.py#L27-L39)

#### Parameters

- **self**


- **kwargs**


### *func* returns.Returns.**signature**

> [Source: ../../miko/parsers/returns.py @ line 42-44](../../miko/parsers/returns.py#L42-L44)

The signature of the callable, if provided

#### Parameters

- **self**

