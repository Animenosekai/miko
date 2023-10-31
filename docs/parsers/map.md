# *module* **map**

> [Source: ../../miko/parsers/map.py @ line 0](../../miko/parsers/map.py#L0)

This defines the listed element parsers  
"Mapped elements" refers to docstring paragraphs where multiple items can be mapped

## Imports

- [../../miko/parsers/parser.py](../../miko/parsers/parser.py): As `Parser`, `Element`

## Examples

### Example 1

```python
>>> def func():
...     """
...     Paragraph
...     ---------
...     element1: options1, options2
...         element1 description
...     element2: options1, options2
...         element2 description
...     """
```

## *class* **MapElement**

> [Source: ../../miko/parsers/map.py @ line 24-96](../../miko/parsers/map.py#L24-L96)

An item in the map

### *attr* MapElement.**name**

> [Source: ../../miko/parsers/map.py @ line 26](../../miko/parsers/map.py#L26)

> Type: `str`

The name for the map item

### *attr* MapElement.**options**

> [Source: ../../miko/parsers/map.py @ line 29](../../miko/parsers/map.py#L29)

> Type: `Set`

The options for the element

#### Examples

##### Example 1

```python
element1: option1, option2
          ^^^^^^^  ^^^^^^^
    (content)
```

### *func* MapElement.**extend_options**

> [Source: ../../miko/parsers/map.py @ line 55-64](../../miko/parsers/map.py#L55-L64)

Extends the options with the provided values

#### Parameters

- **options**: `Iterable[str]`, `Iterable`
  - Options to add to the options


### *func* MapElement.**render_options**

> [Source: ../../miko/parsers/map.py @ line 66-68](../../miko/parsers/map.py#L66-L68)

Renders the options

#### Returns

- `str`

### *func* MapElement.**dumps**

> [Source: ../../miko/parsers/map.py @ line 70-88](../../miko/parsers/map.py#L70-L88)

Renders the element

#### Parameters

- **indent**: `int`
  - Default Value: `4`
  - The indentation level


#### Returns

- `str`

### *func* MapElement.**exported**

> [Source: ../../miko/parsers/map.py @ line 91-96](../../miko/parsers/map.py#L91-L96)

## *const* **T**

> [Source: ../../miko/parsers/map.py @ line 99](../../miko/parsers/map.py#L99)

## *class* **MapParser**

> [Source: ../../miko/parsers/map.py @ line 102-175](../../miko/parsers/map.py#L102-L175)

A parser for map paragraphs

### Raises

- `KeyError`

### *attr* MapParser.**element**

> [Source: ../../miko/parsers/map.py @ line 104](../../miko/parsers/map.py#L104)

### *func* MapParser.**extend**

> [Source: ../../miko/parsers/map.py @ line 108-134](../../miko/parsers/map.py#L108-L134)

Parses and adds new content to the paragraph

#### Parameters

- **content**: `str`
  - The content to add to the paragraph


### *func* MapParser.**dumps**

> [Source: ../../miko/parsers/map.py @ line 136-146](../../miko/parsers/map.py#L136-L146)

#### Parameters

- **indent**: `int`
  - Default Value: `4`


#### Returns

- `str`
