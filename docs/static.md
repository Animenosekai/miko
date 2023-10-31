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

> [Source: ../miko/static.py @ line 125-177](../miko/static.py#L125-L177)

Returns the correct value from the given expression

### Parameters

- **builtin**: `bool`
  - Default Value: `True`
  - If the element should be already loaded or coming from a builtin module
to be fully loaded. Otherwise a dot path will be returned.
See `get_element` for more information on loading arbitrary elements.


- **expr**: `ast.expr`
  - This value is **optional**
  - The expression to get the value from


### Returns

- `None`
    - If it couldn't get the value

- `str`
    - The value for the expression

## *func* **signature_from_ast**

> [Source: ../miko/static.py @ line 180-271](../miko/static.py#L180-L271)

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

> [Source: ../miko/static.py @ line 274-286](../miko/static.py#L274-L286)

Exports the data of an AST node

### Parameters

- **node**: `AST`


### Returns

- `dict`

## *const* **NodeType**

> [Source: ../miko/static.py @ line 289](../miko/static.py#L289)

## *class* **Element**

> [Source: ../miko/static.py @ line 293-370](../miko/static.py#L293-L370)

A documented element

### *attr* Element.**node**

> [Source: ../miko/static.py @ line 295](../miko/static.py#L295)

> Type: `NodeType`

The node

### *attr* Element.**parents**

> [Source: ../miko/static.py @ line 297](../miko/static.py#L297)

> Type: `List`

The nesting where the element was defined

### *attr* Element.**docstring**

> [Source: ../miko/static.py @ line 299](../miko/static.py#L299)

> Type: `Optional`

The docstring element

### *attr* Element.**filename**

> [Source: ../miko/static.py @ line 302](../miko/static.py#L302)

> Type: `Optional`

The filename where the element was defined, for easier debugging

### *attr* Element.**safe**

> [Source: ../miko/static.py @ line 304](../miko/static.py#L304)

> Type: `bool`

If the annotations and exceptions should be safely loaded

### *func* Element.**signature**

> [Source: ../miko/static.py @ line 308-313](../miko/static.py#L308-L313)

If available, the signature of the node

### *func* Element.**raised**

> [Source: ../miko/static.py @ line 316-320](../miko/static.py#L316-L320)

### *func* Element.**document**

> [Source: ../miko/static.py @ line 322-328](../miko/static.py#L322-L328)

Documents the element

#### Parameters

- **kwargs**


### *func* Element.**documentation**

> [Source: ../miko/static.py @ line 331-339](../miko/static.py#L331-L339)

Returns the documentation for the node

### *func* Element.**export**

> [Source: ../miko/static.py @ line 341-352](../miko/static.py#L341-L352)

Exports the data

#### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


### *func* Element.**exported**

> [Source: ../miko/static.py @ line 355-357](../miko/static.py#L355-L357)

Exported data

### *func* Element.**is_private**

> [Source: ../miko/static.py @ line 360-370](../miko/static.py#L360-L370)

If the element is private

## *class* **ConstantElement**

> [Source: ../miko/static.py @ line 374-385](../miko/static.py#L374-L385)

A constant element

### *func* ConstantElement.**document**

> [Source: ../miko/static.py @ line 378-381](../miko/static.py#L378-L381)

Documents the element

#### Parameters

- **kwargs**


### *func* ConstantElement.**documentation**

> [Source: ../miko/static.py @ line 384-385](../miko/static.py#L384-L385)

## *func* **get_elements**

> [Source: ../miko/static.py @ line 388-522](../miko/static.py#L388-L522)

Gets all of the elements which could be documented inside the AST

### Parameters

- **filename**
  - This value is **optional**


- **node**: `AST`, `ast.AST`
  - The Abstract Syntax Tree element to search into


- **parents**: `None`, `typing.List[ast.AST]`
  - This value is **optional**
  - The parents of the current element


- **safe**: `bool`
  - Default Value: `True`
  - If the annotations and exceptions should be safely loaded


## *func* **clean_elements**

> [Source: ../miko/static.py @ line 525-566](../miko/static.py#L525-L566)

Cleans up the given elements

### Parameters

- **elements**: `list`


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


## *func* **clean**

> [Source: ../miko/static.py @ line 569-577](../miko/static.py#L569-L577)

Cleans up the source code

### Parameters

- **filename**
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

> [Source: ../miko/static.py @ line 580-587](../miko/static.py#L580-L587)

Gathers information on the different elements of the source code

### Parameters

- **filename**
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

> [Source: ../miko/static.py @ line 591-612](../miko/static.py#L591-L612)

The location of an import

### *attr* ImportLocation.**file**

> [Source: ../miko/static.py @ line 593](../miko/static.py#L593)

> Type: `Path`

The file where the import is located

### *attr* ImportLocation.**name**

> [Source: ../miko/static.py @ line 595](../miko/static.py#L595)

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

> [Source: ../miko/static.py @ line 611](../miko/static.py#L611)

> Type: `None`

The node of the import, used to retrieve the location within the file

## *const* **PYTHON_EXTENSIONS**

> [Source: ../miko/static.py @ line 615](../miko/static.py#L615)

## *class* **Import**

> [Source: ../miko/static.py @ line 619-625](../miko/static.py#L619-L625)

An import

### *attr* Import.**file**

> [Source: ../miko/static.py @ line 621](../miko/static.py#L621)

> Type: `Path`

The file which is imported

### *attr* Import.**locations**

> [Source: ../miko/static.py @ line 623](../miko/static.py#L623)

> Type: `List`

The locations of the import

## *const* **IMPORTS_CACHE**

> [Source: ../miko/static.py @ line 628](../miko/static.py#L628)

> Type: `Dict`

## *func* **resolve_import**

> [Source: ../miko/static.py @ line 631-768](../miko/static.py#L631-L768)

Resolves an import

### Parameters

- **context**
  - This value is **optional**


- **level**: `int`
  - This value is **optional**
  - The level of the import


- **module**: `None`, `str`
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

> [Source: ../miko/static.py @ line 771-925](../miko/static.py#L771-L925)

Gets all imported files

### Parameters

- **boundary**: `None`, `pathlib.Path`
  - This value is **optional**
  - The boundary of the imports.
This is used to bound the search to only a certain directory.
If an import is made from outside the boundary, it is ignored.


- **file**: `Path`
  - The file to get imports from


- **no_fail**: `bool`
  - Default Value: `True`
  - Whether to raise an error if an import cannot be resolved


- **parents**
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

> [Source: ../miko/static.py @ line 928-972](../miko/static.py#L928-L972)

### Parameters

- **ignored**
  - This value is **optional**


- **node**: `AST`


- **safe**: `bool`
  - Default Value: `True`

