# *module* **miko**

> [Source: ../miko/miko.py @ line 0](../miko/miko.py#L0)

miko.py  
Contains the main code for the Miko documentation style

## Imports

- [../miko/parsers/__init__.py](../miko/parsers/__init__.py): As `parsers`

## *class* **Callable**

> [Source: ../miko/miko.py @ line 15-120](../miko/miko.py#L15-L120)

Retrieves information on a given function

### Raises

- `TypeError`

### *class* Callable.**Source**

> [Source: ../miko/miko.py @ line 19-26](../miko/miko.py#L19-L26)

Stores information on the source of a callable

#### *attr* Callable.Source.**filename**

> [Source: ../miko/miko.py @ line 21](../miko/miko.py#L21)

> Type: `str`

The filename where the callable was defined

#### *attr* Callable.Source.**line**

> [Source: ../miko/miko.py @ line 23](../miko/miko.py#L23)

> Type: `int`

The line where the callable was defined

#### *attr* Callable.Source.**name**

> [Source: ../miko/miko.py @ line 25](../miko/miko.py#L25)

> Type: `str`

The original name of the callable

### *func* Callable.**local_variables**

> [Source: ../miko/miko.py @ line 56-58](../miko/miko.py#L56-L58)

Returns the local variables of the function

#### Returns

- `tuple`

### *func* Callable.**parameters**

> [Source: ../miko/miko.py @ line 61-63](../miko/miko.py#L61-L63)

Returns the parameters of the function

#### Returns

- `dict`

### *func* Callable.**return_annotation**

> [Source: ../miko/miko.py @ line 66-68](../miko/miko.py#L66-L68)

Returns the return annotation of the function

#### Returns

- `Any`

### *func* Callable.**get_code**

> [Source: ../miko/miko.py @ line 71-96](../miko/miko.py#L71-L96)

Returns the __code__ object of a given callable object.

#### Parameters

- **obj**: `Any`, `Callable`
  - The object to get the __code__ from


#### Returns

- `CodeType`
    - The __code__ object

- `code`

#### Raises

- `TypeError`

### *func* Callable.**is_method**

> [Source: ../miko/miko.py @ line 100-102](../miko/miko.py#L100-L102)

Returns whether the callable is a method of an instantiated object or not

### *func* Callable.**is_function**

> [Source: ../miko/miko.py @ line 105-107](../miko/miko.py#L105-L107)

Returns whether the callable is a function or not

### *func* Callable.**is_class**

> [Source: ../miko/miko.py @ line 110-112](../miko/miko.py#L110-L112)

Returns whether the callable is a class or not

### *func* Callable.**source_code**

> [Source: ../miko/miko.py @ line 115-117](../miko/miko.py#L115-L117)

Returns the source code for the callable

## *const* **Function**

> [Source: ../miko/miko.py @ line 124](../miko/miko.py#L124)

## *class* **BaseDocumentation**

> [Source: ../miko/miko.py @ line 127-314](../miko/miko.py#L127-L314)

The base docstring parser

### *attr* BaseDocumentation.**original**

> [Source: ../miko/miko.py @ line 130](../miko/miko.py#L130)

> Type: `str`

Original text

### *attr* BaseDocumentation.**description**

> [Source: ../miko/miko.py @ line 132](../miko/miko.py#L132)

> Type: `str`

The description

### *func* BaseDocumentation.**dumps**

> [Source: ../miko/miko.py @ line 259-295](../miko/miko.py#L259-L295)

Returns a clean docstring

#### Parameters

- **indent**: `int`
  - Default Value: `4`


### *func* BaseDocumentation.**exported**

> [Source: ../miko/miko.py @ line 304-314](../miko/miko.py#L304-L314)

The exported data

## *class* **ConstantDocumentation**

> [Source: ../miko/miko.py @ line 317-339](../miko/miko.py#L317-L339)

The documentation for a constant

### *attr* ConstantDocumentation.**deprecated**

> [Source: ../miko/miko.py @ line 321](../miko/miko.py#L321)

> Type: `parsers.deprecated.Deprecated`

A flag to indicate if the element is deprecated

### *attr* ConstantDocumentation.**notes**

> [Source: ../miko/miko.py @ line 325](../miko/miko.py#L325)

> Type: `parsers.notes.Notes`

Notes about the element

### *attr* ConstantDocumentation.**warnings**

> [Source: ../miko/miko.py @ line 327](../miko/miko.py#L327)

> Type: `parsers.warnings.Warnings`

Warnings about the element

### *attr* ConstantDocumentation.**important**

> [Source: ../miko/miko.py @ line 329](../miko/miko.py#L329)

> Type: `parsers.important.Important`

Important notes about the element

### *attr* ConstantDocumentation.**examples**

> [Source: ../miko/miko.py @ line 332](../miko/miko.py#L332)

> Type: `parsers.example.Example`

Examples of usage

### *attr* ConstantDocumentation.**changelog**

> [Source: ../miko/miko.py @ line 336](../miko/miko.py#L336)

> Type: `parsers.changelog.Changelog`

Changelog of the element

### *attr* ConstantDocumentation.**copyright**

> [Source: ../miko/miko.py @ line 338](../miko/miko.py#L338)

> Type: `parsers.copyright.Copyright`

Copyright notes for the element

## *class* **Documentation**

> [Source: ../miko/miko.py @ line 342-372](../miko/miko.py#L342-L372)

The full built-in documentation

### *attr* Documentation.**deprecated**

> [Source: ../miko/miko.py @ line 346](../miko/miko.py#L346)

> Type: `parsers.deprecated.Deprecated`

A flag to indicate if the element is deprecated

### *attr* Documentation.**notes**

> [Source: ../miko/miko.py @ line 350](../miko/miko.py#L350)

> Type: `parsers.notes.Notes`

Notes about the element

### *attr* Documentation.**warnings**

> [Source: ../miko/miko.py @ line 352](../miko/miko.py#L352)

> Type: `parsers.warnings.Warnings`

Warnings about the element

### *attr* Documentation.**important**

> [Source: ../miko/miko.py @ line 354](../miko/miko.py#L354)

> Type: `parsers.important.Important`

Important notes about the element

### *attr* Documentation.**examples**

> [Source: ../miko/miko.py @ line 357](../miko/miko.py#L357)

> Type: `parsers.example.Example`

Examples of usage

### *attr* Documentation.**parameters**

> [Source: ../miko/miko.py @ line 361](../miko/miko.py#L361)

> Type: `parsers.parameters.Parameters`

Parameters for the callable

### *attr* Documentation.**returns**

> [Source: ../miko/miko.py @ line 363](../miko/miko.py#L363)

> Type: `parsers.returns.Returns`

Return value for the callable

### *attr* Documentation.**yields**

> [Source: ../miko/miko.py @ line 365](../miko/miko.py#L365)

> Type: `parsers.yields.Yields`

Return value for the callable

### *attr* Documentation.**raises**

> [Source: ../miko/miko.py @ line 367](../miko/miko.py#L367)

> Type: `parsers.raises.Raises`

Raisable exception by the callable

### *attr* Documentation.**changelog**

> [Source: ../miko/miko.py @ line 369](../miko/miko.py#L369)

> Type: `parsers.changelog.Changelog`

Changelog of the element

### *attr* Documentation.**copyright**

> [Source: ../miko/miko.py @ line 371](../miko/miko.py#L371)

> Type: `parsers.copyright.Copyright`

Copyright notes for the element

## *const* **Docs**

> [Source: ../miko/miko.py @ line 376](../miko/miko.py#L376)
