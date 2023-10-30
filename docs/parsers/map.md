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

> [Source: ../../miko/parsers/map.py @ line 23-95](../../miko/parsers/map.py#L23-L95)

An item in the map

### *attr* MapElement.**name**

> [Source: ../../miko/parsers/map.py @ line 25](../../miko/parsers/map.py#L25)

> Type: `str`

The name for the map item

### *attr* MapElement.**options**

> [Source: ../../miko/parsers/map.py @ line 28](../../miko/parsers/map.py#L28)

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

> [Source: ../../miko/parsers/map.py @ line 54-63](../../miko/parsers/map.py#L54-L63)

Extends the options with the provided values

#### Parameters

- **options**: `Iterable[str]`, `Iterable`
  - Options to add to the options


### *func* MapElement.**render_options**

> [Source: ../../miko/parsers/map.py @ line 65-67](../../miko/parsers/map.py#L65-L67)

Renders the options

#### Returns

- `str`

### *func* MapElement.**dumps**

> [Source: ../../miko/parsers/map.py @ line 69-87](../../miko/parsers/map.py#L69-L87)

Renders the element

#### Parameters

- **indent**: `int`
  - Default Value: `4`
  - The indentation level


#### Returns

- `str`

### *func* MapElement.**exported**

> [Source: ../../miko/parsers/map.py @ line 90-95](../../miko/parsers/map.py#L90-L95)

## *const* **T**

> [Source: ../../miko/parsers/map.py @ line 98](../../miko/parsers/map.py#L98)

## *func* **split_options**

> [Source: ../../miko/parsers/map.py @ line 101-128](../../miko/parsers/map.py#L101-L128)

Retrieves the different options for an element

### Parameters

- **value**: `str`


### Returns

- `list`

## *class* **MapParser**

> [Source: ../../miko/parsers/map.py @ line 131-204](../../miko/parsers/map.py#L131-L204)

A parser for map paragraphs

### Raises

- `KeyError`

### *attr* MapParser.**element**

> [Source: ../../miko/parsers/map.py @ line 133](../../miko/parsers/map.py#L133)

### *func* MapParser.**extend**

> [Source: ../../miko/parsers/map.py @ line 137-163](../../miko/parsers/map.py#L137-L163)

Parses and adds new content to the paragraph

#### Parameters

- **content**: `str`
  - The content to add to the paragraph


### *func* MapParser.**dumps**

> [Source: ../../miko/parsers/map.py @ line 165-175](../../miko/parsers/map.py#L165-L175)

#### Parameters

- **indent**: `int`
  - Default Value: `4`


#### Returns

- `str`
