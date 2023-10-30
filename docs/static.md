# *module* **static**

> [Source: ../miko/static.py @ line 0](../miko/static.py#L0)

Implementation of miko's static code analysis tools  
This is used to retrieve information on the different elements of the code  
without having to run it.

## *func* static.**get_element**

> [Source: ../miko/static.py @ line 27-96](../miko/static.py#L27-L96)

Get a element from its dot path

### Parameters

- **dot_path**: str
  - The dot path of the element to get


- **builtin**: bool
  - This value is **optional**
  - If the element should be already loaded or coming from a builtin module.
This avoids loading unknown code, which could lead to unexpected results.


### Returns

- Any
    - Any element pointed by the dot path

> **Warning**
> Keep in mind that the full dot path needs to be provided

## *func* static.**get_dot_path**

> [Source: ../miko/static.py @ line 99-118](../miko/static.py#L99-L118)

Returns the dot path for a given attribute

### Parameters

- **attr**: ast.attribute
  - The attribute to get the whole dot path from


### Returns

- str
    - The dot path

## *func* static.**get_value**

> [Source: ../miko/static.py @ line 121-172](../miko/static.py#L121-L172)

Returns the correct value from the given expression

### Parameters

- **expr**: ast.expr
  - This value is **optional**
  - The expression to get the value from


- **builtin**: bool
  - This value is **optional**
  - If the element should be already loaded or coming from a builtin module
to be fully loaded. Otherwise a dot path will be returned.
See `get_element` for more information on loading arbitrary elements.


### Returns

- str
    - The value for the expression

- None
    - If it couldn't get the value

## *func* static.**signature_from_ast**

> [Source: ../miko/static.py @ line 175-266](../miko/static.py#L175-L266)

Computes the signature of a function from its AST

### Parameters

- **node**:  ast.functiondef, ast.asyncfunctiondef 
  - The node to get the signature from


- **builtin**: bool
  - This value is **optional**
  - If annotations should be already loaded or
coming from a builtin module to be fully loaded.
Otherwise a dot path will be returned.
See get_element for more information on loading arbitrary elements.


### Returns

- Signature
    - 

- inspect.Signature
    - This the signature of the function,
retrieved without ever running the code

## *func* static.**export_node**

> [Source: ../miko/static.py @ line 269-281](../miko/static.py#L269-L281)

Exports the data of an AST node

### Parameters

- **node**: AST


## *const* static.**NodeType**

> [Source: ../miko/static.py @ line 284](../miko/static.py#L284)

## *class* static.**Element**

> [Source: ../miko/static.py @ line 288-335](../miko/static.py#L288-L335)

A documented element

### *const* static.Element.**node**

> [Source: ../miko/static.py @ line 290](../miko/static.py#L290)

The node

### *const* static.Element.**parents**

> [Source: ../miko/static.py @ line 292](../miko/static.py#L292)

The nesting where the element was defined

### *const* static.Element.**docstring**

> [Source: ../miko/static.py @ line 294](../miko/static.py#L294)

The docstring element

### *const* static.Element.**safe_annotations**

> [Source: ../miko/static.py @ line 297](../miko/static.py#L297)

If the annotations should be safely loaded

### *func* static.Element.**signature**

> [Source: ../miko/static.py @ line 301-306](../miko/static.py#L301-L306)

If available, the signature of the node

#### Parameters

- **self**


### *func* static.Element.**document**

> [Source: ../miko/static.py @ line 308-312](../miko/static.py#L308-L312)

Documents the element

#### Parameters

- **self**


- **kwargs**


### *func* static.Element.**documentation**

> [Source: ../miko/static.py @ line 315-317](../miko/static.py#L315-L317)

Returns the documentation for the node

#### Parameters

- **self**


### *func* static.Element.**export**

> [Source: ../miko/static.py @ line 319-330](../miko/static.py#L319-L330)

Exports the data

#### Parameters

- **self**


- **indent**: int
  - Default Value: `4`


- **kwargs**


### *func* static.Element.**exported**

> [Source: ../miko/static.py @ line 333-335](../miko/static.py#L333-L335)

Exported data

#### Parameters

- **self**


## *class* static.**ConstantElement**

> [Source: ../miko/static.py @ line 339-350](../miko/static.py#L339-L350)

A constant element

### *func* static.ConstantElement.**document**

> [Source: ../miko/static.py @ line 343-346](../miko/static.py#L343-L346)

Documents the element

#### Parameters

- **self**


- **kwargs**


### *func* static.ConstantElement.**documentation**

> [Source: ../miko/static.py @ line 349-350](../miko/static.py#L349-L350)

#### Parameters

- **self**


## *func* static.**get_elements**

> [Source: ../miko/static.py @ line 353-485](../miko/static.py#L353-L485)

Gets all of the elements which could be documented inside the AST

### Parameters

- **node**: AST, ast.ast
  - The Abstract Syntax Tree element to search into


- **parents**: ], [, i, l, ., s, g, p, a, None, t, n, y
  - Default Value: `none`
  - The parents of the current element


- **safe_annotations**: bool
  - This value is **optional**
  - If the annotations should be safely loaded


## *func* static.**clean_elements**

> [Source: ../miko/static.py @ line 488-529](../miko/static.py#L488-L529)

Cleans up the given elements

### Parameters

- **elements**


- **indent**: int
  - Default Value: `4`


- **kwargs**


## *func* static.**clean**

> [Source: ../miko/static.py @ line 532-540](../miko/static.py#L532-L540)

Cleans up the source code

### Parameters

- **source**: str


- **indent**: int
  - Default Value: `4`


- **safe_annotations**: bool
  - This value is **optional**


- **kwargs**


### Returns

- str
    - 

## *func* static.**info**

> [Source: ../miko/static.py @ line 543-550](../miko/static.py#L543-L550)

Gathers information on the different elements of the source code

### Parameters

- **source**: str


- **indent**: int
  - Default Value: `4`


- **safe_annotations**: bool
  - This value is **optional**


- **kwargs**


## *class* static.**ImportLocation**

> [Source: ../miko/static.py @ line 554-575](../miko/static.py#L554-L575)

The location of an import

### *const* static.ImportLocation.**file**

> [Source: ../miko/static.py @ line 556](../miko/static.py#L556)

The file where the import is located

### *const* static.ImportLocation.**name**

> [Source: ../miko/static.py @ line 558](../miko/static.py#L558)

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

### *const* static.ImportLocation.**node**

> [Source: ../miko/static.py @ line 574](../miko/static.py#L574)

The node of the import, used to retrieve the location within the file

## *const* static.**PYTHON_EXTENSIONS**

> [Source: ../miko/static.py @ line 578](../miko/static.py#L578)

## *class* static.**Import**

> [Source: ../miko/static.py @ line 582-588](../miko/static.py#L582-L588)

An import

### *const* static.Import.**file**

> [Source: ../miko/static.py @ line 584](../miko/static.py#L584)

The file which is imported

### *const* static.Import.**locations**

> [Source: ../miko/static.py @ line 586](../miko/static.py#L586)

The locations of the import

## *const* static.**IMPORTS_CACHE**

> [Source: ../miko/static.py @ line 591](../miko/static.py#L591)

## *func* static.**resolve_import**

> [Source: ../miko/static.py @ line 594-731](../miko/static.py#L594-L731)

Resolves an import

### Parameters

- **name**: str
  - The name of the import


- **module**: s, r, None, t
  - Default Value: `none`
  - The module of the import


- **level**: int
  - This value is **optional**
  - The level of the import


- **safe**: bool
  - Default Value: `True`
  - Whether to use the safe method of resolving imports
or the unsafe method of resolving imports


- **context**
  - This value is **optional**


### Returns

- Path
    - 

## *func* static.**get_imports**

> [Source: ../miko/static.py @ line 734-888](../miko/static.py#L734-L888)

Gets all imported files

### Parameters

- **file**: Path
  - The file to get imports from


- **boundary**: h, i, l, ., b, a, p, None, t
  - Default Value: `none`
  - The boundary of the imports.
This is used to bound the search to only a certain directory.
If an import is made from outside the boundary, it is ignored.


- **recursive**: bool
  - Default Value: `True`
  - Whether to get imports recursively


- **no_fail**: bool
  - This value is **optional**
  - Whether to raise an error if an import cannot be resolved


- **safe**: bool
  - Default Value: `True`
  - Whether to use the safe method of resolving imports
or the unsafe method of resolving imports


- **parents**
  - This value is **optional**

