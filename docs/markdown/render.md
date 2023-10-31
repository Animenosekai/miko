# *module* **render**

> [Source: ../../miko/markdown/render.py @ line 0](../../miko/markdown/render.py#L0)

This module contains the functions to render down the  
documentationn elements to markdown

## *func* **heading**

> [Source: ../../miko/markdown/render.py @ line 14-18](../../miko/markdown/render.py#L14-L18)

Renders a heading of the given level

### Parameters

- **base**: `int`
  - This value is **optional**


- **level**: `int`


- **message**: `str`


## *func* **example**

> [Source: ../../miko/markdown/render.py @ line 21-32](../../miko/markdown/render.py#L21-L32)

Renders an example code block

### Parameters

- **example**: `str`


## *func* **accentuated**

> [Source: ../../miko/markdown/render.py @ line 35-40](../../miko/markdown/render.py#L35-L40)

Renders a markdown accentuated note

### Parameters

- **level**: `str`


- **message**: `str`


## *func* **note**

> [Source: ../../miko/markdown/render.py @ line 43-45](../../miko/markdown/render.py#L43-L45)

Renders a markdown note

### Parameters

- **message**: `str`


## *func* **important**

> [Source: ../../miko/markdown/render.py @ line 48-50](../../miko/markdown/render.py#L48-L50)

Renders a markdown important note

### Parameters

- **message**: `str`


## *func* **warning**

> [Source: ../../miko/markdown/render.py @ line 53-55](../../miko/markdown/render.py#L53-L55)

Renders a markdown warning

### Parameters

- **message**: `str`


## *func* **deprecated**

> [Source: ../../miko/markdown/render.py @ line 58-60](../../miko/markdown/render.py#L58-L60)

Renders a markdown deprecation warning

### Parameters

- **element_type**: `str`
  - Default Value: `value`


## *func* **relative_link**

> [Source: ../../miko/markdown/render.py @ line 63-79](../../miko/markdown/render.py#L63-L79)

### Parameters

- **base_dir**: `Optional`
  - This value is **optional**


- **source_file**: `Path`


## *func* **source_link**

> [Source: ../../miko/markdown/render.py @ line 82-107](../../miko/markdown/render.py#L82-L107)

Renders a markdown source link

### Parameters

- **base_dir**: `Optional`, `Path`
  - This value is **optional**
  - The base directory of the output directory to use for relative paths


- **end**: `int`
  - The end line number


- **source_file**: `Path`
  - The path to the source file


- **start**: `int`
  - The start line number


### Returns

- `str`
    - The markdown source link

## *func* **imports**

> [Source: ../../miko/markdown/render.py @ line 110-119](../../miko/markdown/render.py#L110-L119)

Renders a markdown imports

### Parameters

- **base_dir**: `Optional`
  - This value is **optional**


- **imports**: `list`


## *func* **changelog**

> [Source: ../../miko/markdown/render.py @ line 122-136](../../miko/markdown/render.py#L122-L136)

Renders a markdown changelog

### Parameters

- **elements**: `parsers.changelog.Changelog`


## *func* **copyright**

> [Source: ../../miko/markdown/render.py @ line 139-159](../../miko/markdown/render.py#L139-L159)

Renders a markdown copyright

### Parameters

- **elements**: `parsers.copyright.Copyright`


## *func* **stringify_type**

> [Source: ../../miko/markdown/render.py @ line 162-166](../../miko/markdown/render.py#L162-L166)

Stringifies a type

### Parameters

- **t**: `Any`


## *func* **parameters**

> [Source: ../../miko/markdown/render.py @ line 169-193](../../miko/markdown/render.py#L169-L193)

Renders a markdown parameters

### Parameters

- **parameters**: `parsers.parameters.Parameters`


## *func* **returns**

> [Source: ../../miko/markdown/render.py @ line 196-205](../../miko/markdown/render.py#L196-L205)

Renders a markdown returns

### Parameters

- **returns**: `parsers.returns.Returns`


## *func* **yields**

> [Source: ../../miko/markdown/render.py @ line 208-217](../../miko/markdown/render.py#L208-L217)

Renders a markdown returns

### Parameters

- **yields**: `parsers.yields.Yields`


## *func* **raises**

> [Source: ../../miko/markdown/render.py @ line 220-229](../../miko/markdown/render.py#L220-L229)

Renders a markdown raises

### Parameters

- **raises**: `parsers.raises.Raises`


## *func* **description**

> [Source: ../../miko/markdown/render.py @ line 232-234](../../miko/markdown/render.py#L232-L234)

Renders a markdown description

### Parameters

- **description**: `str`

