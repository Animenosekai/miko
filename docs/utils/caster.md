# *module* **caster**

> [Source: ../../miko/utils/caster.py @ line 0](../../miko/utils/caster.py#L0)

Casts element to the right type

## Imports

- [../../miko/utils/empty.py](../../miko/utils/empty.py): As `is_empty`

## *class* **Callable**

> [Source: ../../miko/utils/caster.py @ line 18-39](../../miko/utils/caster.py#L18-L39)

Represents a callable type

### *attr* Callable.**arg_types**

> **Note**
> This value is of type `None`

> [Source: ../../miko/utils/caster.py @ line 20](../../miko/utils/caster.py#L20)

The types for the arguments

### *attr* Callable.**return_type**

> **Note**
> This value is of type `None`

> [Source: ../../miko/utils/caster.py @ line 22](../../miko/utils/caster.py#L22)

The type for the return value

## *const* **Type**

> [Source: ../../miko/utils/caster.py @ line 42](../../miko/utils/caster.py#L42)

## *func* **try_retrieve_type**

> [Source: ../../miko/utils/caster.py @ line 45-132](../../miko/utils/caster.py#L45-L132)

Tries to retrieve the types from a string

### Parameters

- **filename**
  - This value is **optional**


- **value**


## *func* **try_cast**

> [Source: ../../miko/utils/caster.py @ line 135-168](../../miko/utils/caster.py#L135-L168)

Tries casting the given value

### Parameters

- **types**: `set`
  - The types to try casting to


- **value**: `str`
  - The value to cast

