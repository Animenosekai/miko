# *module* **static**

> [Source: ../miko/static.py @ line 0](../miko/static.py#L0)

Implementation of miko's static code analysis tools  
This is used to retrieve information on the different elements of the code  
without having to run it.

## *func* **get_element**

> [Source: ../miko/static.py @ line 27-96](../miko/static.py#L27-L96)

Get a element from its dot path

### Parameters

- **dot_path**: `str`
  - The dot path of the element to get


- **builtin**: `bool`
  - This value is **optional**
  - If the element should be already loaded or coming from a builtin module.
This avoids loading unknown code, which could lead to unexpected results.


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

- **expr**: `ast.expr`
  - This value is **optional**
  - The expression to get the value from


- **builtin**: `bool`
  - This value is **optional**
  - If the element should be already loaded or coming from a builtin module
to be fully loaded. Otherwise a dot path will be returned.
See `get_element` for more information on loading arbitrary elements.


### Returns

- `str`
    - The value for the expression

- `None`
    - If it couldn't get the value

## *func* **signature_from_ast**

> [Source: ../miko/static.py @ line 175-266](../miko/static.py#L175-L266)

Computes the signature of a function from its AST

### Parameters

- **node**: `ast.asyncfunctiondef `, ` ast.functiondef`
  - The node to get the signature from


- **builtin**: `bool`
  - This value is **optional**
  - If annotations should be already loaded or
coming from a builtin module to be fully loaded.
Otherwise a dot path will be returned.
See get_element for more information on loading arbitrary elements.


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

> [Source: ../miko/static.py @ line 288-349](../miko/static.py#L288-L349)

A documented element

### *const* Element.**node**

> [Source: ../miko/static.py @ line 290](../miko/static.py#L290)

The node

### *const* Element.**parents**

> [Source: ../miko/static.py @ line 292](../miko/static.py#L292)

The nesting where the element was defined

### *const* Element.**docstring**

> [Source: ../miko/static.py @ line 294](../miko/static.py#L294)

The docstring element

### *const* Element.**safe**

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

## *class* **ConstantElement**

> [Source: ../miko/static.py @ line 353-364](../miko/static.py#L353-L364)

A constant element

### *func* ConstantElement.**document**

> [Source: ../miko/static.py @ line 357-360](../miko/static.py#L357-L360)

Documents the element

#### Parameters

- **kwargs**


### *func* ConstantElement.**documentation**

> [Source: ../miko/static.py @ line 363-364](../miko/static.py#L363-L364)

## *func* **get_elements**

> [Source: ../miko/static.py @ line 367-499](../miko/static.py#L367-L499)

Gets all of the elements which could be documented inside the AST

### Parameters

- **node**: `ast.ast`, `AST`
  - The Abstract Syntax Tree element to search into


- **parents**: `[`, `s`, `t`, `n`, `y`, `p`, `]`, `None`, `l`, `.`, `a`, `g`, `i`
  - Default Value: `none`
  - The parents of the current element


- **safe**: `bool`
  - This value is **optional**
  - If the annotations and exceptions should be safely loaded


## *func* **clean_elements**

> [Source: ../miko/static.py @ line 502-543](../miko/static.py#L502-L543)

Cleans up the given elements

### Parameters

- **elements**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


## *func* **clean**

> [Source: ../miko/static.py @ line 546-554](../miko/static.py#L546-L554)

Cleans up the source code

### Parameters

- **source**: `str`


- **indent**: `int`
  - Default Value: `4`


- **safe**: `bool`
  - This value is **optional**


- **kwargs**


### Returns

- `str`

## *func* **info**

> [Source: ../miko/static.py @ line 557-564](../miko/static.py#L557-L564)

Gathers information on the different elements of the source code

### Parameters

- **source**: `str`


- **indent**: `int`
  - Default Value: `4`


- **safe**: `bool`
  - This value is **optional**


- **kwargs**


## *class* **ImportLocation**

> [Source: ../miko/static.py @ line 568-589](../miko/static.py#L568-L589)

The location of an import

### *const* ImportLocation.**file**

> [Source: ../miko/static.py @ line 570](../miko/static.py#L570)

The file where the import is located

### *const* ImportLocation.**name**

> [Source: ../miko/static.py @ line 572](../miko/static.py#L572)

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

### *const* ImportLocation.**node**

> [Source: ../miko/static.py @ line 588](../miko/static.py#L588)

The node of the import, used to retrieve the location within the file

## *const* **PYTHON_EXTENSIONS**

> [Source: ../miko/static.py @ line 592](../miko/static.py#L592)

## *class* **Import**

> [Source: ../miko/static.py @ line 596-602](../miko/static.py#L596-L602)

An import

### *const* Import.**file**

> [Source: ../miko/static.py @ line 598](../miko/static.py#L598)

The file which is imported

### *const* Import.**locations**

> [Source: ../miko/static.py @ line 600](../miko/static.py#L600)

The locations of the import

## *const* **IMPORTS_CACHE**

> [Source: ../miko/static.py @ line 605](../miko/static.py#L605)

## *func* **resolve_import**

> [Source: ../miko/static.py @ line 608-745](../miko/static.py#L608-L745)

Resolves an import

### Parameters

- **name**: `str`
  - The name of the import


- **module**: `r`, `None`, `s`, `t`
  - Default Value: `none`
  - The module of the import


- **level**: `int`
  - This value is **optional**
  - The level of the import


- **safe**: `bool`
  - Default Value: `True`
  - Whether to use the safe method of resolving imports
or the unsafe method of resolving imports


- **context**
  - This value is **optional**


### Returns

- `Path`

## *func* **get_imports**

> [Source: ../miko/static.py @ line 748-902](../miko/static.py#L748-L902)

Gets all imported files

### Parameters

- **file**: `Path`
  - The file to get imports from


- **boundary**: `b`, `.`, `p`, `h`, `i`, `None`, `l`, `a`, `t`
  - Default Value: `none`
  - The boundary of the imports.
This is used to bound the search to only a certain directory.
If an import is made from outside the boundary, it is ignored.


- **recursive**: `bool`
  - Default Value: `True`
  - Whether to get imports recursively


- **no_fail**: `bool`
  - This value is **optional**
  - Whether to raise an error if an import cannot be resolved


- **safe**: `bool`
  - Default Value: `True`
  - Whether to use the safe method of resolving imports
or the unsafe method of resolving imports


- **parents**
  - This value is **optional**


## *func* **get_raised**

> [Source: ../miko/static.py @ line 905-936](../miko/static.py#L905-L936)

### Parameters

- **node**: `AST`


- **safe**: `bool`
  - Default Value: `True`


- **ignored**
  - This value is **optional**

