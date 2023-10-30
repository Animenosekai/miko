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

> [Source: ../miko/static.py @ line 288-341](../miko/static.py#L288-L341)

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

### *const* Element.**safe_annotations**

> [Source: ../miko/static.py @ line 297](../miko/static.py#L297)

If the annotations should be safely loaded

### *func* Element.**signature**

> [Source: ../miko/static.py @ line 301-306](../miko/static.py#L301-L306)

If available, the signature of the node

### *func* Element.**document**

> [Source: ../miko/static.py @ line 308-312](../miko/static.py#L308-L312)

Documents the element

#### Parameters

- **kwargs**


### *func* Element.**documentation**

> [Source: ../miko/static.py @ line 315-323](../miko/static.py#L315-L323)

Returns the documentation for the node

### *func* Element.**export**

> [Source: ../miko/static.py @ line 325-336](../miko/static.py#L325-L336)

Exports the data

#### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


### *func* Element.**exported**

> [Source: ../miko/static.py @ line 339-341](../miko/static.py#L339-L341)

Exported data

## *class* **ConstantElement**

> [Source: ../miko/static.py @ line 345-356](../miko/static.py#L345-L356)

A constant element

### *func* ConstantElement.**document**

> [Source: ../miko/static.py @ line 349-352](../miko/static.py#L349-L352)

Documents the element

#### Parameters

- **kwargs**


### *func* ConstantElement.**documentation**

> [Source: ../miko/static.py @ line 355-356](../miko/static.py#L355-L356)

## *func* **get_elements**

> [Source: ../miko/static.py @ line 359-491](../miko/static.py#L359-L491)

Gets all of the elements which could be documented inside the AST

### Parameters

- **node**: `AST`, `ast.ast`
  - The Abstract Syntax Tree element to search into


- **parents**: `i`, `n`, `p`, `y`, `l`, `]`, `.`, `[`, `t`, `None`, `a`, `g`, `s`
  - Default Value: `none`
  - The parents of the current element


- **safe_annotations**: `bool`
  - This value is **optional**
  - If the annotations should be safely loaded


## *func* **clean_elements**

> [Source: ../miko/static.py @ line 494-535](../miko/static.py#L494-L535)

Cleans up the given elements

### Parameters

- **elements**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


## *func* **clean**

> [Source: ../miko/static.py @ line 538-546](../miko/static.py#L538-L546)

Cleans up the source code

### Parameters

- **source**: `str`


- **indent**: `int`
  - Default Value: `4`


- **safe_annotations**: `bool`
  - This value is **optional**


- **kwargs**


### Returns

- `str`

## *func* **info**

> [Source: ../miko/static.py @ line 549-556](../miko/static.py#L549-L556)

Gathers information on the different elements of the source code

### Parameters

- **source**: `str`


- **indent**: `int`
  - Default Value: `4`


- **safe_annotations**: `bool`
  - This value is **optional**


- **kwargs**


## *class* **ImportLocation**

> [Source: ../miko/static.py @ line 560-581](../miko/static.py#L560-L581)

The location of an import

### *const* ImportLocation.**file**

> [Source: ../miko/static.py @ line 562](../miko/static.py#L562)

The file where the import is located

### *const* ImportLocation.**name**

> [Source: ../miko/static.py @ line 564](../miko/static.py#L564)

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

> [Source: ../miko/static.py @ line 580](../miko/static.py#L580)

The node of the import, used to retrieve the location within the file

## *const* **PYTHON_EXTENSIONS**

> [Source: ../miko/static.py @ line 584](../miko/static.py#L584)

## *class* **Import**

> [Source: ../miko/static.py @ line 588-594](../miko/static.py#L588-L594)

An import

### *const* Import.**file**

> [Source: ../miko/static.py @ line 590](../miko/static.py#L590)

The file which is imported

### *const* Import.**locations**

> [Source: ../miko/static.py @ line 592](../miko/static.py#L592)

The locations of the import

## *const* **IMPORTS_CACHE**

> [Source: ../miko/static.py @ line 597](../miko/static.py#L597)

## *func* **resolve_import**

> [Source: ../miko/static.py @ line 600-737](../miko/static.py#L600-L737)

Resolves an import

### Parameters

- **name**: `str`
  - The name of the import


- **module**: `t`, `None`, `s`, `r`
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

> [Source: ../miko/static.py @ line 740-894](../miko/static.py#L740-L894)

Gets all imported files

### Parameters

- **file**: `Path`
  - The file to get imports from


- **boundary**: `p`, `i`, `l`, `.`, `h`, `t`, `None`, `a`, `b`
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

