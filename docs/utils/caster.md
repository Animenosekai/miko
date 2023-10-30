# *module* **caster**

> [Source: ../../miko/utils/caster.py @ line 0](../../miko/utils/caster.py#L0)

Casts element to the right type

## *func* caster.**try_retrieve_type**

> [Source: ../../miko/utils/caster.py @ line 14-70](../../miko/utils/caster.py#L14-L70)

Tries to retrieve the types from a string

### Parameters

- **value**


## *func* caster.**try_cast**

> [Source: ../../miko/utils/caster.py @ line 73-106](../../miko/utils/caster.py#L73-L106)

Tries casting the given value

### Parameters

- **value**: str
  - The value to cast


- **types**: set[str, (str) -> any]
  - The types to try casting to
