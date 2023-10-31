# *module* **static**

> [Source: ../miko/static.py @ line 0](../miko/static.py#L0)

Implementation of miko's static code analysis tools  
This is used to retrieve information on the different elements of the code  
without having to run it.

## Imports

- [../miko/__init__.py](../miko/__init__.py): As `miko`

## *func* **get_element**

> [Source: ../miko/static.py @ line 27-96](../miko/static.py#L27-L96)

Get a element from its dot path

### Parameters

- **builtin**: `bool`
  - Default Value: `True`
  - If the element should be already loaded or coming from a builtin module.
This avoids loading unknown code, which could lead to unexpected results.


- **dot_path**: `str`
  - The dot path of the element to get


### Returns

- `Any`
    - Any element pointed by the dot path

### Raises

- `ValueError`

> **Warning**
> Keep in mind that the full dot path needs to be provided

## *func* **get_dot_path**

> [Source: ../miko/static.py @ line 99-122](../miko/static.py#L99-L122)

Returns the dot path for a given attribute

### Parameters

- **attr**: `ast.Attribute`, `expr`
  - The attribute to get the whole dot path from


### Returns

- `str`
    - The dot path

### Raises

- `ValueError`

## *func* **get_value**

> [Source: ../miko/static.py @ line 125-210](../miko/static.py#L125-L210)

Returns the correct value from the given expression

### Parameters

- **builtin**: `bool`
  - Default Value: `True`
  - If the element should be already loaded or coming from a builtin module
to be fully loaded. Otherwise a dot path will be returned.
See `get_element` for more information on loading arbitrary elements.


- **expr**: `NoneType`, `ast.expr`, `expr`
  - This value is **optional**
  - The expression to get the value from


### Returns

- `Any`

- `None`
    - If it couldn't get the value

- `NoneType`

- `str`
    - The value for the expression

## *func* **signature_from_ast**

> [Source: ../miko/static.py @ line 213-304](../miko/static.py#L213-L304)

Computes the signature of a function from its AST

### Parameters

- **builtin**: `bool`
  - Default Value: `True`
  - If annotations should be already loaded or
coming from a builtin module to be fully loaded.
Otherwise a dot path will be returned.
See get_element for more information on loading arbitrary elements.


- **node**: `ast.AsyncFunctionDef`, `ast.FunctionDef`
  - The node to get the signature from


### Returns

- `Signature`

- `inspect.Signature`
    - This the signature of the function,
retrieved without ever running the code

## *func* **export_node**

> [Source: ../miko/static.py @ line 307-319](../miko/static.py#L307-L319)

Exports the data of an AST node

### Parameters

- **node**: `AST`


### Returns

- `dict`

## *const* **NodeType**

> [Source: ../miko/static.py @ line 322](../miko/static.py#L322)

## *class* **Element**

> [Source: ../miko/static.py @ line 326-403](../miko/static.py#L326-L403)

A documented element

### *attr* Element.**node**

> [Source: ../miko/static.py @ line 328](../miko/static.py#L328)

> Type: `NodeType`

The node

### *attr* Element.**parents**

> [Source: ../miko/static.py @ line 330](../miko/static.py#L330)

> Type: `List`

The nesting where the element was defined

### *attr* Element.**docstring**

> [Source: ../miko/static.py @ line 332](../miko/static.py#L332)

> Type: `Optional`

The docstring element

### *attr* Element.**filename**

> [Source: ../miko/static.py @ line 335](../miko/static.py#L335)

> Type: `Optional`

The filename where the element was defined, for easier debugging

### *attr* Element.**safe**

> [Source: ../miko/static.py @ line 337](../miko/static.py#L337)

> Type: `bool`

If the annotations and exceptions should be safely loaded

### *property* Element.**signature**

> [Source: ../miko/static.py @ line 341-346](../miko/static.py#L341-L346)

If available, the signature of the node

#### Returns

- `NoneType`

- `Signature`

### *property* Element.**raised**

> [Source: ../miko/static.py @ line 349-353](../miko/static.py#L349-L353)

### *func* Element.**document**

> [Source: ../miko/static.py @ line 355-361](../miko/static.py#L355-L361)

Documents the element

#### Parameters

- **kwargs**


### *property* Element.**documentation**

> [Source: ../miko/static.py @ line 364-372](../miko/static.py#L364-L372)

Returns the documentation for the node

### *func* Element.**export**

> [Source: ../miko/static.py @ line 374-385](../miko/static.py#L374-L385)

Exports the data

#### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


### *property* Element.**exported**

> [Source: ../miko/static.py @ line 388-390](../miko/static.py#L388-L390)

Exported data

### *property* Element.**is_private**

> [Source: ../miko/static.py @ line 393-403](../miko/static.py#L393-L403)

If the element is private

## *class* **ConstantElement**

> [Source: ../miko/static.py @ line 407-418](../miko/static.py#L407-L418)

A constant element

### *func* ConstantElement.**document**

> [Source: ../miko/static.py @ line 411-414](../miko/static.py#L411-L414)

Documents the element

#### Parameters

- **kwargs**


### *property* ConstantElement.**documentation**

> [Source: ../miko/static.py @ line 417-418](../miko/static.py#L417-L418)

## *func* **get_elements**

> [Source: ../miko/static.py @ line 421-555](../miko/static.py#L421-L555)

Gets all of the elements which could be documented inside the AST

### Parameters

- **filename**: `NoneType`, `str`
  - This value is **optional**


- **node**: `AST`, `ast.AST`
  - The Abstract Syntax Tree element to search into


- **parents**: `NoneType`, `None`, `list`, `typing.List[ast.AST]`
  - This value is **optional**
  - The parents of the current element


- **safe**: `bool`
  - Default Value: `True`
  - If the annotations and exceptions should be safely loaded


## *func* **clean_elements**

> [Source: ../miko/static.py @ line 558-599](../miko/static.py#L558-L599)

Cleans up the given elements

### Parameters

- **elements**: `list`


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


## *func* **clean**

> [Source: ../miko/static.py @ line 602-610](../miko/static.py#L602-L610)

Cleans up the source code

### Parameters

- **filename**: `NoneType`, `str`
  - This value is **optional**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


- **safe**: `bool`
  - Default Value: `True`


- **source**: `str`


### Returns

- `str`

## *func* **info**

> [Source: ../miko/static.py @ line 613-620](../miko/static.py#L613-L620)

Gathers information on the different elements of the source code

### Parameters

- **filename**: `NoneType`, `str`
  - This value is **optional**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


- **safe**: `bool`
  - Default Value: `True`


- **source**: `str`


### Returns

- `list`

## *class* **ImportLocation**

> [Source: ../miko/static.py @ line 624-645](../miko/static.py#L624-L645)

The location of an import

### *attr* ImportLocation.**file**

> [Source: ../miko/static.py @ line 626](../miko/static.py#L626)

> Type: `Path`

The file where the import is located

### *attr* ImportLocation.**name**

> [Source: ../miko/static.py @ line 628](../miko/static.py#L628)

> Type: `str`

The name of the import.  
This is the name of the variable where the import is stored.

#### Examples

##### Example 1

```python
>>> import x
# name == "x"
>>> import x.y
# name == "x.y"
>>> from x import y
# name == "y"
>>> from w.x import y as z
# name == "z"
```

### *attr* ImportLocation.**node**

> [Source: ../miko/static.py @ line 644](../miko/static.py#L644)

> Type: `None`

The node of the import, used to retrieve the location within the file

## *const* **PYTHON_EXTENSIONS**

> [Source: ../miko/static.py @ line 648](../miko/static.py#L648)

## *class* **Import**

> [Source: ../miko/static.py @ line 652-658](../miko/static.py#L652-L658)

An import

### *attr* Import.**file**

> [Source: ../miko/static.py @ line 654](../miko/static.py#L654)

> Type: `Path`

The file which is imported

### *attr* Import.**locations**

> [Source: ../miko/static.py @ line 656](../miko/static.py#L656)

> Type: `List`

The locations of the import

## *const* **IMPORTS_CACHE**

> [Source: ../miko/static.py @ line 661](../miko/static.py#L661)

> Type: `Dict`

## *func* **resolve_import**

> [Source: ../miko/static.py @ line 664-801](../miko/static.py#L664-L801)

Resolves an import

### Parameters

- **context**: `NoneType`, `Path`
  - This value is **optional**


- **level**: `int`
  - This value is **optional**
  - The level of the import


- **module**: `NoneType`, `None`, `str`
  - This value is **optional**
  - The module of the import


- **name**: `str`
  - The name of the import


- **safe**: `bool`
  - Default Value: `True`
  - Whether to use the safe method of resolving imports
or the unsafe method of resolving imports


### Returns

- `Path`

### Raises

- `ImportError`

- `ValueError`

## *func* **get_imports**

> [Source: ../miko/static.py @ line 804-958](../miko/static.py#L804-L958)

Gets all imported files

### Parameters

- **boundary**: `NoneType`, `None`, `Path`, `pathlib.Path`
  - This value is **optional**
  - The boundary of the imports.
This is used to bound the search to only a certain directory.
If an import is made from outside the boundary, it is ignored.


- **file**: `Path`
  - The file to get imports from


- **no_fail**: `bool`
  - Default Value: `True`
  - Whether to raise an error if an import cannot be resolved


- **parents**: `NoneType`, `set`
  - This value is **optional**


- **recursive**: `bool`
  - Default Value: `True`
  - Whether to get imports recursively


- **safe**: `bool`
  - Default Value: `True`
  - Whether to use the safe method of resolving imports
or the unsafe method of resolving imports


### Returns

- `list`

### Raises

- `ImportError`

## *func* **get_raised**

> [Source: ../miko/static.py @ line 961-1005](../miko/static.py#L961-L1005)

### Parameters

- **ignored**: `NoneType`, `list`
  - This value is **optional**


- **node**: `AST`


- **safe**: `bool`
  - Default Value: `True`

