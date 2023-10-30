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
  - This value is **optional**
  - If the element should be already loaded or coming from a builtin module.
This avoids loading unknown code, which could lead to unexpected results.


- **dot_path**: `str`
  - The dot path of the element to get


### Returns

- `Any`
    - Any element pointed by the dot path

> **Warning**
> Keep in mind that the full dot path needs to be provided

## *func* **get_dot_path**

> [Source: ../miko/static.py @ line 99-118](../miko/static.py#L99-L118)

Returns the dot path for a given attribute

### Parameters

- **attr**: `ast.attribute`
  - The attribute to get the whole dot path from


### Returns

- `str`
    - The dot path

## *func* **get_value**

> [Source: ../miko/static.py @ line 121-172](../miko/static.py#L121-L172)

Returns the correct value from the given expression

### Parameters

- **builtin**: `bool`
  - This value is **optional**
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

> [Source: ../miko/static.py @ line 175-266](../miko/static.py#L175-L266)

Computes the signature of a function from its AST

### Parameters

- **builtin**: `bool`
  - This value is **optional**
  - If annotations should be already loaded or
coming from a builtin module to be fully loaded.
Otherwise a dot path will be returned.
See get_element for more information on loading arbitrary elements.


- **node**: ` ast.functiondef`, `ast.asyncfunctiondef `
  - The node to get the signature from


### Returns

- `Signature`

- `inspect.Signature`
    - This the signature of the function,
retrieved without ever running the code

## *func* **export_node**

> [Source: ../miko/static.py @ line 269-281](../miko/static.py#L269-L281)

Exports the data of an AST node

### Parameters

- **node**: `AST`


## *const* **NodeType**

> [Source: ../miko/static.py @ line 284](../miko/static.py#L284)

## *class* **Element**

> [Source: ../miko/static.py @ line 288-362](../miko/static.py#L288-L362)

A documented element

### *attr* Element.**node**

> [Source: ../miko/static.py @ line 290](../miko/static.py#L290)

The node

### *attr* Element.**parents**

> [Source: ../miko/static.py @ line 292](../miko/static.py#L292)

The nesting where the element was defined

### *attr* Element.**docstring**

> [Source: ../miko/static.py @ line 294](../miko/static.py#L294)

The docstring element

### *attr* Element.**safe**

> [Source: ../miko/static.py @ line 297](../miko/static.py#L297)

If the annotations and exceptions should be safely loaded

### *func* Element.**signature**

> [Source: ../miko/static.py @ line 301-306](../miko/static.py#L301-L306)

If available, the signature of the node

### *func* Element.**raised**

> [Source: ../miko/static.py @ line 309-313](../miko/static.py#L309-L313)

### *func* Element.**document**

> [Source: ../miko/static.py @ line 315-320](../miko/static.py#L315-L320)

Documents the element

#### Parameters

- **kwargs**


### *func* Element.**documentation**

> [Source: ../miko/static.py @ line 323-331](../miko/static.py#L323-L331)

Returns the documentation for the node

### *func* Element.**export**

> [Source: ../miko/static.py @ line 333-344](../miko/static.py#L333-L344)

Exports the data

#### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


### *func* Element.**exported**

> [Source: ../miko/static.py @ line 347-349](../miko/static.py#L347-L349)

Exported data

### *func* Element.**is_private**

> [Source: ../miko/static.py @ line 352-362](../miko/static.py#L352-L362)

If the element is private

## *class* **ConstantElement**

> [Source: ../miko/static.py @ line 366-377](../miko/static.py#L366-L377)

A constant element

### *func* ConstantElement.**document**

> [Source: ../miko/static.py @ line 370-373](../miko/static.py#L370-L373)

Documents the element

#### Parameters

- **kwargs**


### *func* ConstantElement.**documentation**

> [Source: ../miko/static.py @ line 376-377](../miko/static.py#L376-L377)

## *func* **get_elements**

> [Source: ../miko/static.py @ line 380-512](../miko/static.py#L380-L512)

Gets all of the elements which could be documented inside the AST

### Parameters

- **node**: `AST`, `ast.ast`
  - The Abstract Syntax Tree element to search into


- **parents**: `t`, `p`, `i`, `y`, `l`, `a`, `[`, `g`, `None`, `]`, `.`, `s`, `n`
  - Default Value: `none`
  - The parents of the current element


- **safe**: `bool`
  - This value is **optional**
  - If the annotations and exceptions should be safely loaded


## *func* **clean_elements**

> [Source: ../miko/static.py @ line 515-556](../miko/static.py#L515-L556)

Cleans up the given elements

### Parameters

- **elements**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


## *func* **clean**

> [Source: ../miko/static.py @ line 559-567](../miko/static.py#L559-L567)

Cleans up the source code

### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


- **safe**: `bool`
  - This value is **optional**


- **source**: `str`


### Returns

- `str`

## *func* **info**

> [Source: ../miko/static.py @ line 570-577](../miko/static.py#L570-L577)

Gathers information on the different elements of the source code

### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


- **safe**: `bool`
  - This value is **optional**


- **source**: `str`


## *class* **ImportLocation**

> [Source: ../miko/static.py @ line 581-602](../miko/static.py#L581-L602)

The location of an import

### *attr* ImportLocation.**file**

> [Source: ../miko/static.py @ line 583](../miko/static.py#L583)

The file where the import is located

### *attr* ImportLocation.**name**

> [Source: ../miko/static.py @ line 585](../miko/static.py#L585)

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

> [Source: ../miko/static.py @ line 601](../miko/static.py#L601)

The node of the import, used to retrieve the location within the file

## *const* **PYTHON_EXTENSIONS**

> [Source: ../miko/static.py @ line 605](../miko/static.py#L605)

## *class* **Import**

> [Source: ../miko/static.py @ line 609-615](../miko/static.py#L609-L615)

An import

### *attr* Import.**file**

> [Source: ../miko/static.py @ line 611](../miko/static.py#L611)

The file which is imported

### *attr* Import.**locations**

> [Source: ../miko/static.py @ line 613](../miko/static.py#L613)

The locations of the import

## *const* **IMPORTS_CACHE**

> [Source: ../miko/static.py @ line 618](../miko/static.py#L618)

## *func* **resolve_import**

> [Source: ../miko/static.py @ line 621-758](../miko/static.py#L621-L758)

Resolves an import

### Parameters

- **context**
  - This value is **optional**


- **level**: `int`
  - This value is **optional**
  - The level of the import


- **module**: `t`, `None`, `s`, `r`
  - Default Value: `none`
  - The module of the import


- **name**: `str`
  - The name of the import


- **safe**: `bool`
  - Default Value: `True`
  - Whether to use the safe method of resolving imports
or the unsafe method of resolving imports


### Returns

- `Path`

## *func* **get_imports**

> [Source: ../miko/static.py @ line 761-915](../miko/static.py#L761-L915)

Gets all imported files

### Parameters

- **boundary**: `p`, `t`, `i`, `b`, `l`, `a`, `None`, `.`, `h`
  - Default Value: `none`
  - The boundary of the imports.
This is used to bound the search to only a certain directory.
If an import is made from outside the boundary, it is ignored.


- **file**: `Path`
  - The file to get imports from


- **no_fail**: `bool`
  - This value is **optional**
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


## *func* **get_raised**

> [Source: ../miko/static.py @ line 918-949](../miko/static.py#L918-L949)

### Parameters

- **ignored**
  - This value is **optional**


- **node**: `AST`


- **safe**: `bool`
  - Default Value: `True`

