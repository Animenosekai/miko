# *module* **parser**

> [Source: ../../miko/parsers/parser.py @ line 0](../../miko/parsers/parser.py#L0)

Defines the base parser

## *class* **Element**

> [Source: ../../miko/parsers/parser.py @ line 7-47](../../miko/parsers/parser.py#L7-L47)

Represents an element in a docstring paragraph

### *attr* Element.**body**

> Type: `str`
> [Source: ../../miko/parsers/parser.py @ line 9](../../miko/parsers/parser.py#L9)

The body of the element

#### Examples

##### Example 1

```python
element1: option1, option2
    This is a long body
    ^^^^^^^^^^^^^^^^^^^
```

### *attr* Element.**extra_arguments**

> Type: `Dict`
> [Source: ../../miko/parsers/parser.py @ line 20](../../miko/parsers/parser.py#L20)

The extra arguments passed in with the parser

### *func* Element.**append_body**

> [Source: ../../miko/parsers/parser.py @ line 27-40](../../miko/parsers/parser.py#L27-L40)

Appends the given value to the body of the element

#### Parameters

- **value**: `str`
  - The string to append to the body


### *func* Element.**exported**

> [Source: ../../miko/parsers/parser.py @ line 43-47](../../miko/parsers/parser.py#L43-L47)

The exported data

## *const* **T**

> [Source: ../../miko/parsers/parser.py @ line 50](../../miko/parsers/parser.py#L50)

## *class* **Parser**

> [Source: ../../miko/parsers/parser.py @ line 53-113](../../miko/parsers/parser.py#L53-L113)

The base class for a parser

### *attr* Parser.**names**

> Type: `List`
> [Source: ../../miko/parsers/parser.py @ line 55](../../miko/parsers/parser.py#L55)

The names of the section (will be normalized)

### *attr* Parser.**element**

> Type: `Type`
> [Source: ../../miko/parsers/parser.py @ line 57](../../miko/parsers/parser.py#L57)

The element type

### *attr* Parser.**elements**

> Type: `List`
> [Source: ../../miko/parsers/parser.py @ line 59](../../miko/parsers/parser.py#L59)

Elements parsed in the docstring paragraph

### *attr* Parser.**extra_arguments**

> Type: `Dict`
> [Source: ../../miko/parsers/parser.py @ line 61](../../miko/parsers/parser.py#L61)

The extra arguments passed in with the parser

### *func* Parser.**name**

> [Source: ../../miko/parsers/parser.py @ line 70-74](../../miko/parsers/parser.py#L70-L74)

The default name of the section

### *func* Parser.**dumps**

> [Source: ../../miko/parsers/parser.py @ line 76-79](../../miko/parsers/parser.py#L76-L79)

Renders the docstring back

#### Parameters

- **indent**: `int`
  - Default Value: `4`


#### Returns

- `str`

### *func* Parser.**exported**

> [Source: ../../miko/parsers/parser.py @ line 105-113](../../miko/parsers/parser.py#L105-L113)

The exported data
