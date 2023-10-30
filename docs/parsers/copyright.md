# *module* **copyright**

> [Source: ../../miko/parsers/copyright.py @ line 0](../../miko/parsers/copyright.py#L0)

Parser for the `Copyright` paragraph

## Imports

- [../../miko/parsers/map.py](../../miko/parsers/map.py): As `MapParser`, `MapElement`

## Examples

### Example 1

```python
>>> def func():
...     """
...     Copyright
...     ---------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
```

## *class* **License**

> [Source: ../../miko/parsers/copyright.py @ line 20-72](../../miko/parsers/copyright.py#L20-L72)

A license in the `Copyright` section

### *func* License.**license**

> [Source: ../../miko/parsers/copyright.py @ line 23-28](../../miko/parsers/copyright.py#L23-L28)

#### Returns

- `Optional`

### *func* License.**year_from**

> [Source: ../../miko/parsers/copyright.py @ line 31-40](../../miko/parsers/copyright.py#L31-L40)

#### Returns

- `Optional`

### *func* License.**year_to**

> [Source: ../../miko/parsers/copyright.py @ line 43-52](../../miko/parsers/copyright.py#L43-L52)

#### Returns

- `Optional`

### *func* License.**render_options**

> [Source: ../../miko/parsers/copyright.py @ line 54-63](../../miko/parsers/copyright.py#L54-L63)

#### Returns

- `str`

### *func* License.**exported**

> [Source: ../../miko/parsers/copyright.py @ line 66-72](../../miko/parsers/copyright.py#L66-L72)

## *class* **Copyright**

> [Source: ../../miko/parsers/copyright.py @ line 75-78](../../miko/parsers/copyright.py#L75-L78)

Parser for the `Copyright` paragraph

### *attr* Copyright.**names**

> [Source: ../../miko/parsers/copyright.py @ line 77](../../miko/parsers/copyright.py#L77)

### *attr* Copyright.**element**

> [Source: ../../miko/parsers/copyright.py @ line 78](../../miko/parsers/copyright.py#L78)
