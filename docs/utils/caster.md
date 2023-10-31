# *module* **caster**

> [Source: ../../miko/utils/caster.py @ line 0](../../miko/utils/caster.py#L0)

Casts element to the right type

## Imports

- [../../miko/utils/empty.py](../../miko/utils/empty.py): As `is_empty`

## *func* **stringify**

> [Source: ../../miko/utils/caster.py @ line 18-22](../../miko/utils/caster.py#L18-L22)

Stringifies the given type

### Parameters

- **t**


## *func* **split_options**

> [Source: ../../miko/utils/caster.py @ line 25-52](../../miko/utils/caster.py#L25-L52)

Retrieves the different options for an element

### Parameters

- **sep**: `str`
  - Default Value: `,`


- **value**: `str`


### Returns

- `list`

## *class* **Callable**

> [Source: ../../miko/utils/caster.py @ line 56-71](../../miko/utils/caster.py#L56-L71)

Represents a callable type

### *attr* Callable.**arg_types**

> [Source: ../../miko/utils/caster.py @ line 58](../../miko/utils/caster.py#L58)

> Type: `Tuple`

The types for the arguments

### *attr* Callable.**return_type**

> [Source: ../../miko/utils/caster.py @ line 60](../../miko/utils/caster.py#L60)

> Type: `Tuple`

The type for the return value

## *const* **Type**

> [Source: ../../miko/utils/caster.py @ line 74](../../miko/utils/caster.py#L74)

## *func* **try_retrieve_type**

> [Source: ../../miko/utils/caster.py @ line 77-181](../../miko/utils/caster.py#L77-L181)

Tries to retrieve the types from a string

### Parameters

- **filename**: `NoneType`, `str`
  - This value is **optional**


- **value**: `str`, `type`


### Returns

- `list`

### Raises

- `SyntaxError`

## *func* **try_cast**

> [Source: ../../miko/utils/caster.py @ line 184-217](../../miko/utils/caster.py#L184-L217)

Tries casting the given value

### Parameters

- **types**: `set`
  - The types to try casting to


- **value**: `str`
  - The value to cast


### Returns

- `Any`

- `str`
