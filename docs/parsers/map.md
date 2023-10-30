# *module* **map**

> [Source: ../../miko/parsers/map.py @ line 0](../../miko/parsers/map.py#L0)

This defines the listed element parsers  
"Mapped elements" refers to docstring paragraphs where multiple items can be mapped

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

## *class* map.**MapElement**

> [Source: ../../miko/parsers/map.py @ line 23-91](../../miko/parsers/map.py#L23-L91)

An item in the map

### *const* map.MapElement.**name**

> [Source: ../../miko/parsers/map.py @ line 25](../../miko/parsers/map.py#L25)

The name for the map item

### *const* map.MapElement.**options**

> [Source: ../../miko/parsers/map.py @ line 28](../../miko/parsers/map.py#L28)

The options for the element

#### Examples

##### Example 1

```python
element1: option1, option2
          ^^^^^^^  ^^^^^^^
    (content)
```

### *func* map.MapElement.**__init__**

> [Source: ../../miko/parsers/map.py @ line 39-44](../../miko/parsers/map.py#L39-L44)

#### Parameters

- **self**


- **name**: str


- **options**
  - This value is **optional**


- **kwargs**


### *func* map.MapElement.**_normalize_option**

> [Source: ../../miko/parsers/map.py @ line 46-47](../../miko/parsers/map.py#L46-L47)

#### Parameters

- **self**


- **option**: str


### *func* map.MapElement.**extend_options**

> [Source: ../../miko/parsers/map.py @ line 49-59](../../miko/parsers/map.py#L49-L59)

Extends the options with the provided values

#### Parameters

- **self**


- **options**: iterable[str]
  - Options to add to the options


### *func* map.MapElement.**render_options**

> [Source: ../../miko/parsers/map.py @ line 61-63](../../miko/parsers/map.py#L61-L63)

Renders the options

#### Parameters

- **self**


#### Returns

- str
    - 

### *func* map.MapElement.**dumps**

> [Source: ../../miko/parsers/map.py @ line 65-83](../../miko/parsers/map.py#L65-L83)

Renders the element

#### Parameters

- **self**


- **indent**: int
  - Default Value: `4`
  - The indentation level


#### Returns

- str
    - 

### *func* map.MapElement.**exported**

> [Source: ../../miko/parsers/map.py @ line 86-91](../../miko/parsers/map.py#L86-L91)

#### Parameters

- **self**


## *const* map.**T**

> [Source: ../../miko/parsers/map.py @ line 94](../../miko/parsers/map.py#L94)

## *class* map.**MapParser**

> [Source: ../../miko/parsers/map.py @ line 97-170](../../miko/parsers/map.py#L97-L170)

A parser for map paragraphs

### *const* map.MapParser.**element**

> [Source: ../../miko/parsers/map.py @ line 99](../../miko/parsers/map.py#L99)

### *func* map.MapParser.**extend**

> [Source: ../../miko/parsers/map.py @ line 103-129](../../miko/parsers/map.py#L103-L129)

Parses and adds new content to the paragraph

#### Parameters

- **self**


- **content**: str
  - The content to add to the paragraph


### *func* map.MapParser.**dumps**

> [Source: ../../miko/parsers/map.py @ line 131-141](../../miko/parsers/map.py#L131-L141)

#### Parameters

- **self**


- **indent**: int
  - Default Value: `4`


#### Returns

- str
    - 

### *func* map.MapParser.**__getitem__**

> [Source: ../../miko/parsers/map.py @ line 143-149](../../miko/parsers/map.py#L143-L149)

#### Parameters

- **self**


- **key**: str


### *func* map.MapParser.**__setitem__**

> [Source: ../../miko/parsers/map.py @ line 151-158](../../miko/parsers/map.py#L151-L158)

#### Parameters

- **self**


- **key**: str


- **value**: MapElement


### *func* map.MapParser.**__delitem__**

> [Source: ../../miko/parsers/map.py @ line 160-164](../../miko/parsers/map.py#L160-L164)

#### Parameters

- **self**


- **key**: str


### *func* map.MapParser.**__iter__**

> [Source: ../../miko/parsers/map.py @ line 166-167](../../miko/parsers/map.py#L166-L167)

#### Parameters

- **self**


### *func* map.MapParser.**__repr__**

> [Source: ../../miko/parsers/map.py @ line 169-170](../../miko/parsers/map.py#L169-L170)

#### Parameters

- **self**


#### Returns

- str
    - 
