# *module* **raises**

> [Source: ../../miko/parsers/raises.py @ line 0](../../miko/parsers/raises.py#L0)

Parser for the `Raises` paragraph

## Examples

### Example 1

```python
>>> def func():
...     """
...     Raises
...     ---------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
```

## *class* **Raises**

> [Source: ../../miko/parsers/raises.py @ line 19-39](../../miko/parsers/raises.py#L19-L39)

Parser for the `Raises` paragraph

### *const* Raises.**names**

> [Source: ../../miko/parsers/raises.py @ line 21](../../miko/parsers/raises.py#L21)

### *func* Raises.**__init__**

> [Source: ../../miko/parsers/raises.py @ line 24-34](../../miko/parsers/raises.py#L24-L34)

#### Parameters

- **kwargs**


### *func* Raises.**raised**

> [Source: ../../miko/parsers/raises.py @ line 37-39](../../miko/parsers/raises.py#L37-L39)

The raised exceptions
