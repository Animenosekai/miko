# *module* **make**

> [Source: ../../miko/markdown/make.py @ line 0](../../miko/markdown/make.py#L0)

This module contains functions for making documentation from the AST.

## Imports

- [../../miko/markdown/render.py](../../miko/markdown/render.py): As `render`

- [../../miko/markdown/tree.py](../../miko/markdown/tree.py): As `tree`

## *func* **PrivateElement**

> [Source: ../../miko/markdown/make.py @ line 12-14](../../miko/markdown/make.py#L12-L14)

Returns True if the given element is private

### Parameters

- **element**: `static.Element`


## *func* **make_docs**

> [Source: ../../miko/markdown/make.py @ line 17-54](../../miko/markdown/make.py#L17-L54)

Makes the documentation for every file loaded by the entry point

### Parameters

- **element_filter**: `(ForwardRef('static.Element')) -> bool`


- **entry_point**: `Path`


- **file_filter**: `(Path) -> bool`


- **output_dir**: `Path`


- **safe**: `bool`
  - Default Value: `True`


### Raises

- `FileNotFoundError`

> **Note**
> An entry point could be for example the __init__.py file of a library

## *func* **make_module_docs**

> [Source: ../../miko/markdown/make.py @ line 57-73](../../miko/markdown/make.py#L57-L73)

Makes the documentation for a module

### Parameters

- **element_filter**: `(ForwardRef('static.Element')) -> bool`


- **output_file**: `Path`


- **safe**: `bool`
  - Default Value: `True`


- **source_file**: `Path`


## *func* **render_module_docs**

> [Source: ../../miko/markdown/make.py @ line 76-146](../../miko/markdown/make.py#L76-L146)

Makes the documentation for a module

## *func* **render_class_docs**

> [Source: ../../miko/markdown/make.py @ line 149-232](../../miko/markdown/make.py#L149-L232)

## *func* **render_constant_docs**

> [Source: ../../miko/markdown/make.py @ line 235-292](../../miko/markdown/make.py#L235-L292)

Makes the documentation for a constant

### Parameters

- **base_dir**: `NoneType`, `Path`
  - This value is **optional**


- **constant_type**: `str`
  - Default Value: `const`


- **element**: `static.ConstantElement`


- **level**: `int`
  - This value is **optional**


- **parent_path**: `str`
  - This value is **optional**


- **source_file**: `Path`


## *func* **render_function_docs**

> [Source: ../../miko/markdown/make.py @ line 295-373](../../miko/markdown/make.py#L295-L373)

Makes the documentation for a function

### Parameters

- **base_dir**: `NoneType`, `Path`
  - This value is **optional**


- **element**: `static.Element`


- **level**: `int`
  - This value is **optional**


- **parent_path**: `str`
  - This value is **optional**


- **source_file**: `Path`

