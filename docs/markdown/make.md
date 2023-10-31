# *module* **make**

> [Source: ../../miko/markdown/make.py @ line 0](../../miko/markdown/make.py#L0)

This module contains functions for making documentation from the AST.

## *func* **PrivateElement**

> [Source: ../../miko/markdown/make.py @ line 12-14](../../miko/markdown/make.py#L12-L14)

Returns True if the given element is private

### Parameters

- **element**: `static.Element`


## *func* **make_docs**

> [Source: ../../miko/markdown/make.py @ line 17-52](../../miko/markdown/make.py#L17-L52)

Makes the documentation for every file loaded by the entry point

### Parameters

- **element_filter**: `() -> Any`


- **entry_point**: `Path`


- **file_filter**: `() -> Any`


- **output_dir**: `Path`


- **safe**: `bool`
  - Default Value: `True`


### Raises

- `FileNotFoundError`

> **Note**
> An entry point could be for example the __init__.py file of a library

## *func* **make_module_docs**

> [Source: ../../miko/markdown/make.py @ line 55-68](../../miko/markdown/make.py#L55-L68)

Makes the documentation for a module

### Parameters

- **element_filter**: `() -> Any`


- **output_file**: `Path`


- **safe**: `bool`
  - Default Value: `True`


- **source_file**: `Path`


## *func* **render_module_docs**

> [Source: ../../miko/markdown/make.py @ line 71-141](../../miko/markdown/make.py#L71-L141)

Makes the documentation for a module

## *func* **render_class_docs**

> [Source: ../../miko/markdown/make.py @ line 144-227](../../miko/markdown/make.py#L144-L227)

## *func* **render_constant_docs**

> [Source: ../../miko/markdown/make.py @ line 230-287](../../miko/markdown/make.py#L230-L287)

Makes the documentation for a constant

### Parameters

- **base_dir**: `Optional`
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

> [Source: ../../miko/markdown/make.py @ line 290-360](../../miko/markdown/make.py#L290-L360)

Makes the documentation for a function

### Parameters

- **base_dir**: `Optional`
  - This value is **optional**


- **element**: `static.Element`


- **level**: `int`
  - This value is **optional**


- **parent_path**: `str`
  - This value is **optional**


- **source_file**: `Path`

