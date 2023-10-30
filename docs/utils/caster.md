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


## *class* **Callable**

> [Source: ../../miko/utils/caster.py @ line 26-41](../../miko/utils/caster.py#L26-L41)

Represents a callable type

### *attr* Callable.**arg_types**

> Type: `Tuple`
> [Source: ../../miko/utils/caster.py @ line 28](../../miko/utils/caster.py#L28)

The types for the arguments

### *attr* Callable.**return_type**

> Type: `Tuple`
> [Source: ../../miko/utils/caster.py @ line 30](../../miko/utils/caster.py#L30)

The type for the return value

## *const* **Type**

> [Source: ../../miko/utils/caster.py @ line 44](../../miko/utils/caster.py#L44)

## *func* **try_retrieve_type**

> [Source: ../../miko/utils/caster.py @ line 47-147](../../miko/utils/caster.py#L47-L147)

Tries to retrieve the types from a string

### Parameters

- **filename**: `Optional`
  - This value is **optional**


- **value**: `Union`


### Returns

- `list`

## *func* **try_cast**

> [Source: ../../miko/utils/caster.py @ line 150-183](../../miko/utils/caster.py#L150-L183)

Tries casting the given value

### Parameters

- **types**: `set`
  - The types to try casting to


- **value**: `str`
  - The value to cast


### Returns

- `Union`
