# *module* **raises**

> [Source: ../../miko/parsers/raises.py @ line 0](../../miko/parsers/raises.py#L0)

Parser for the `Raises` paragraph

## Imports

- [../../miko/parsers/map.py](../../miko/parsers/map.py): As `MapParser`

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

### *attr* Raises.**names**

> [Source: ../../miko/parsers/raises.py @ line 21](../../miko/parsers/raises.py#L21)

### *property* Raises.**raised**

> [Source: ../../miko/parsers/raises.py @ line 37-39](../../miko/parsers/raises.py#L37-L39)

The raised exceptions
