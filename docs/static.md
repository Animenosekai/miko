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

> [Source: ../miko/static.py @ line 99-122](../miko/static.py#L99-L122)

Returns the dot path for a given attribute

### Parameters

- **attr**: `expr`, `ast.attribute`
  - The attribute to get the whole dot path from


### Returns

- `str`
    - The dot path

## *func* **get_value**

> [Source: ../miko/static.py @ line 125-176](../miko/static.py#L125-L176)

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

> [Source: ../miko/static.py @ line 179-270](../miko/static.py#L179-L270)

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

> [Source: ../miko/static.py @ line 273-285](../miko/static.py#L273-L285)

Exports the data of an AST node

### Parameters

- **node**: `AST`


## *const* **NodeType**

> [Source: ../miko/static.py @ line 288](../miko/static.py#L288)

## *class* **Element**

> [Source: ../miko/static.py @ line 292-366](../miko/static.py#L292-L366)

A documented element

### *attr* Element.**node**

> **Important**
> This attr is of type `NodeType`

> [Source: ../miko/static.py @ line 294](../miko/static.py#L294)

The node

### *attr* Element.**parents**

> **Important**
> This attr is of type `None`

> [Source: ../miko/static.py @ line 296](../miko/static.py#L296)

The nesting where the element was defined

### *attr* Element.**docstring**

> **Important**
> This attr is of type `None`

> [Source: ../miko/static.py @ line 298](../miko/static.py#L298)

The docstring element

### *attr* Element.**safe**

> **Important**
> This attr is of type `bool`

> [Source: ../miko/static.py @ line 301](../miko/static.py#L301)

If the annotations and exceptions should be safely loaded

### *func* Element.**signature**

> [Source: ../miko/static.py @ line 305-310](../miko/static.py#L305-L310)

If available, the signature of the node

### *func* Element.**raised**

> [Source: ../miko/static.py @ line 313-317](../miko/static.py#L313-L317)

### *func* Element.**document**

> [Source: ../miko/static.py @ line 319-324](../miko/static.py#L319-L324)

Documents the element

#### Parameters

- **kwargs**


### *func* Element.**documentation**

> [Source: ../miko/static.py @ line 327-335](../miko/static.py#L327-L335)

Returns the documentation for the node

### *func* Element.**export**

> [Source: ../miko/static.py @ line 337-348](../miko/static.py#L337-L348)

Exports the data

#### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


### *func* Element.**exported**

> [Source: ../miko/static.py @ line 351-353](../miko/static.py#L351-L353)

Exported data

### *func* Element.**is_private**

> [Source: ../miko/static.py @ line 356-366](../miko/static.py#L356-L366)

If the element is private

## *class* **ConstantElement**

> [Source: ../miko/static.py @ line 370-381](../miko/static.py#L370-L381)

A constant element

### *func* ConstantElement.**document**

> [Source: ../miko/static.py @ line 374-377](../miko/static.py#L374-L377)

Documents the element

#### Parameters

- **kwargs**


### *func* ConstantElement.**documentation**

> [Source: ../miko/static.py @ line 380-381](../miko/static.py#L380-L381)

## *func* **get_elements**

> [Source: ../miko/static.py @ line 384-516](../miko/static.py#L384-L516)

Gets all of the elements which could be documented inside the AST

### Parameters

- **node**: `AST`, `ast.ast`
  - The Abstract Syntax Tree element to search into


- **parents**: `i`, `t`, `]`, `[`, `p`, `a`, `g`, `s`, `y`, `None`, `l`, `.`, `n`
  - Default Value: `none`
  - The parents of the current element


- **safe**: `bool`
  - This value is **optional**
  - If the annotations and exceptions should be safely loaded


## *func* **clean_elements**

> [Source: ../miko/static.py @ line 519-560](../miko/static.py#L519-L560)

Cleans up the given elements

### Parameters

- **elements**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


## *func* **clean**

> [Source: ../miko/static.py @ line 563-571](../miko/static.py#L563-L571)

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

> [Source: ../miko/static.py @ line 574-581](../miko/static.py#L574-L581)

Gathers information on the different elements of the source code

### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


- **safe**: `bool`
  - This value is **optional**


- **source**: `str`


## *class* **ImportLocation**

> [Source: ../miko/static.py @ line 585-606](../miko/static.py#L585-L606)

The location of an import

### *attr* ImportLocation.**file**

> **Important**
> This attr is of type `Path`

> [Source: ../miko/static.py @ line 587](../miko/static.py#L587)

The file where the import is located

### *attr* ImportLocation.**name**

> **Important**
> This attr is of type `str`

> [Source: ../miko/static.py @ line 589](../miko/static.py#L589)

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

> **Important**
> This attr is of type `None`

> [Source: ../miko/static.py @ line 605](../miko/static.py#L605)

The node of the import, used to retrieve the location within the file

## *const* **PYTHON_EXTENSIONS**

> [Source: ../miko/static.py @ line 609](../miko/static.py#L609)

## *class* **Import**

> [Source: ../miko/static.py @ line 613-619](../miko/static.py#L613-L619)

An import

### *attr* Import.**file**

> **Important**
> This attr is of type `Path`

> [Source: ../miko/static.py @ line 615](../miko/static.py#L615)

The file which is imported

### *attr* Import.**locations**

> **Important**
> This attr is of type `None`

> [Source: ../miko/static.py @ line 617](../miko/static.py#L617)

The locations of the import

## *const* **IMPORTS_CACHE**

> **Important**
> This const is of type `None`

> [Source: ../miko/static.py @ line 622](../miko/static.py#L622)

## *func* **resolve_import**

> [Source: ../miko/static.py @ line 625-762](../miko/static.py#L625-L762)

Resolves an import

### Parameters

- **context**
  - This value is **optional**


- **level**: `int`
  - This value is **optional**
  - The level of the import


- **module**: `s`, `t`, `r`, `None`
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

> [Source: ../miko/static.py @ line 765-919](../miko/static.py#L765-L919)

Gets all imported files

### Parameters

- **boundary**: `h`, `i`, `t`, `p`, `a`, `b`, `None`, `l`, `.`
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

> [Source: ../miko/static.py @ line 922-953](../miko/static.py#L922-L953)

### Parameters

- **ignored**
  - This value is **optional**


- **node**: `AST`


- **safe**: `bool`
  - Default Value: `True`

