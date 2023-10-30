# *module* **map**

> [Source: ../../miko/parsers/map.py @ line 0](../../miko/parsers/map.py#L0)

This defines the listed element parsers  
"Mapped elements" refers to docstring paragraphs where multiple items can be mapped

## Imports

- [../../miko/parsers/parser.py](../../miko/parsers/parser.py): As `Parser`

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

> [Source: ../../miko/parsers/map.py @ line 23-91](../../miko/parsers/map.py#L23-L91)

An item in the map

### *attr* MapElement.**name**

> **Note**
> This value is of type `str`

> [Source: ../../miko/parsers/map.py @ line 25](../../miko/parsers/map.py#L25)

The name for the map item

### *attr* MapElement.**options**

> **Note**
> This value is of type `None`

> [Source: ../../miko/parsers/map.py @ line 28](../../miko/parsers/map.py#L28)

The options for the element

#### Examples

##### Example 1

```python
element1: option1, option2
          ^^^^^^^  ^^^^^^^
    (content)
```

### *func* MapElement.**extend_options**

> [Source: ../../miko/parsers/map.py @ line 49-59](../../miko/parsers/map.py#L49-L59)

Extends the options with the provided values

#### Parameters

- **options**: `iterable[str]`
  - Options to add to the options


### *func* MapElement.**render_options**

> [Source: ../../miko/parsers/map.py @ line 61-63](../../miko/parsers/map.py#L61-L63)

Renders the options

#### Returns

- `str`

### *func* MapElement.**dumps**

> [Source: ../../miko/parsers/map.py @ line 65-83](../../miko/parsers/map.py#L65-L83)

Renders the element

#### Parameters

- **indent**: `int`
  - Default Value: `4`
  - The indentation level


#### Returns

- `str`

### *func* MapElement.**exported**

> [Source: ../../miko/parsers/map.py @ line 86-91](../../miko/parsers/map.py#L86-L91)

## *const* **T**

> [Source: ../../miko/parsers/map.py @ line 94](../../miko/parsers/map.py#L94)

## *func* **split_options**

> [Source: ../../miko/parsers/map.py @ line 97-124](../../miko/parsers/map.py#L97-L124)

Retrieves the different options for an element

### Parameters

- **value**: `str`


## *class* **MapParser**

> [Source: ../../miko/parsers/map.py @ line 127-200](../../miko/parsers/map.py#L127-L200)

A parser for map paragraphs

### *attr* MapParser.**element**

> [Source: ../../miko/parsers/map.py @ line 129](../../miko/parsers/map.py#L129)

### *func* MapParser.**extend**

> [Source: ../../miko/parsers/map.py @ line 133-159](../../miko/parsers/map.py#L133-L159)

Parses and adds new content to the paragraph

#### Parameters

- **content**: `str`
  - The content to add to the paragraph


### *func* MapParser.**dumps**

> [Source: ../../miko/parsers/map.py @ line 161-171](../../miko/parsers/map.py#L161-L171)

#### Parameters

- **indent**: `int`
  - Default Value: `4`


#### Returns

- `str`
