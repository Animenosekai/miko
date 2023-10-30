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

> [Source: ../miko/static.py @ line 292-369](../miko/static.py#L292-L369)

A documented element

### *attr* Element.**node**

> **Note**
> This value is of type `NodeType`

> [Source: ../miko/static.py @ line 294](../miko/static.py#L294)

The node

### *attr* Element.**parents**

> **Note**
> This value is of type `None`

> [Source: ../miko/static.py @ line 296](../miko/static.py#L296)

The nesting where the element was defined

### *attr* Element.**docstring**

> **Note**
> This value is of type `None`

> [Source: ../miko/static.py @ line 298](../miko/static.py#L298)

The docstring element

### *attr* Element.**filename**

> **Note**
> This value is of type `None`

> [Source: ../miko/static.py @ line 301](../miko/static.py#L301)

The filename where the element was defined, for easier debugging

### *attr* Element.**safe**

> **Note**
> This value is of type `bool`

> [Source: ../miko/static.py @ line 303](../miko/static.py#L303)

If the annotations and exceptions should be safely loaded

### *func* Element.**signature**

> [Source: ../miko/static.py @ line 307-312](../miko/static.py#L307-L312)

If available, the signature of the node

### *func* Element.**raised**

> [Source: ../miko/static.py @ line 315-319](../miko/static.py#L315-L319)

### *func* Element.**document**

> [Source: ../miko/static.py @ line 321-327](../miko/static.py#L321-L327)

Documents the element

#### Parameters

- **kwargs**


### *func* Element.**documentation**

> [Source: ../miko/static.py @ line 330-338](../miko/static.py#L330-L338)

Returns the documentation for the node

### *func* Element.**export**

> [Source: ../miko/static.py @ line 340-351](../miko/static.py#L340-L351)

Exports the data

#### Parameters

- **indent**: `int`
  - Default Value: `4`


- **kwargs**


### *func* Element.**exported**

> [Source: ../miko/static.py @ line 354-356](../miko/static.py#L354-L356)

Exported data

### *func* Element.**is_private**

> [Source: ../miko/static.py @ line 359-369](../miko/static.py#L359-L369)

If the element is private

## *class* **ConstantElement**

> [Source: ../miko/static.py @ line 373-384](../miko/static.py#L373-L384)

A constant element

### *func* ConstantElement.**document**

> [Source: ../miko/static.py @ line 377-380](../miko/static.py#L377-L380)

Documents the element

#### Parameters

- **kwargs**


### *func* ConstantElement.**documentation**

> [Source: ../miko/static.py @ line 383-384](../miko/static.py#L383-L384)

## *func* **get_elements**

> [Source: ../miko/static.py @ line 387-521](../miko/static.py#L387-L521)

Gets all of the elements which could be documented inside the AST

### Parameters

- **filename**
  - This value is **optional**


- **node**: `AST`, `ast.ast`
  - The Abstract Syntax Tree element to search into


- **parents**: `g`, `l`, `]`, `n`, `i`, `y`, `[`, `.`, `s`, `t`, `p`, `None`, `a`
  - Default Value: `none`
  - The parents of the current element


- **safe**: `bool`
  - This value is **optional**
  - If the annotations and exceptions should be safely loaded


## *func* **clean_elements**

> [Source: ../miko/static.py @ line 524-565](../miko/static.py#L524-L565)

Cleans up the given elements

### Parameters

- **elements**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


## *func* **clean**

> [Source: ../miko/static.py @ line 568-576](../miko/static.py#L568-L576)

Cleans up the source code

### Parameters

- **filename**
  - This value is **optional**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


- **safe**: `bool`
  - This value is **optional**


- **source**: `str`


### Returns

- `str`

## *func* **info**

> [Source: ../miko/static.py @ line 579-586](../miko/static.py#L579-L586)

Gathers information on the different elements of the source code

### Parameters

- **filename**
  - This value is **optional**


- **indent**: `int`
  - Default Value: `4`


- **kwargs**


- **safe**: `bool`
  - This value is **optional**


- **source**: `str`


## *class* **ImportLocation**

> [Source: ../miko/static.py @ line 590-611](../miko/static.py#L590-L611)

The location of an import

### *attr* ImportLocation.**file**

> **Note**
> This value is of type `Path`

> [Source: ../miko/static.py @ line 592](../miko/static.py#L592)

The file where the import is located

### *attr* ImportLocation.**name**

> **Note**
> This value is of type `str`

> [Source: ../miko/static.py @ line 594](../miko/static.py#L594)

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

> **Note**
> This value is of type `None`

> [Source: ../miko/static.py @ line 610](../miko/static.py#L610)

The node of the import, used to retrieve the location within the file

## *const* **PYTHON_EXTENSIONS**

> [Source: ../miko/static.py @ line 614](../miko/static.py#L614)

## *class* **Import**

> [Source: ../miko/static.py @ line 618-624](../miko/static.py#L618-L624)

An import

### *attr* Import.**file**

> **Note**
> This value is of type `Path`

> [Source: ../miko/static.py @ line 620](../miko/static.py#L620)

The file which is imported

### *attr* Import.**locations**

> **Note**
> This value is of type `None`

> [Source: ../miko/static.py @ line 622](../miko/static.py#L622)

The locations of the import

## *const* **IMPORTS_CACHE**

> **Note**
> This value is of type `None`

> [Source: ../miko/static.py @ line 627](../miko/static.py#L627)

## *func* **resolve_import**

> [Source: ../miko/static.py @ line 630-767](../miko/static.py#L630-L767)

Resolves an import

### Parameters

- **context**
  - This value is **optional**


- **level**: `int`
  - This value is **optional**
  - The level of the import


- **module**: `t`, `r`, `None`, `s`
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

> [Source: ../miko/static.py @ line 770-924](../miko/static.py#L770-L924)

Gets all imported files

### Parameters

- **boundary**: `l`, `i`, `b`, `.`, `t`, `p`, `h`, `None`, `a`
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

> [Source: ../miko/static.py @ line 927-958](../miko/static.py#L927-L958)

### Parameters

- **ignored**
  - This value is **optional**


- **node**: `AST`


- **safe**: `bool`
  - Default Value: `True`

