# *module* **inline**

> [Source: ../../miko/parsers/inline.py @ line 0](../../miko/parsers/inline.py#L0)

Defines the base class for inline parsers  
Inline sections can be used inline when there  
is no need to have more than a line to describe the section.  
If it requires multiple lines, you can use a syntax similar to the  
map parser one, and start the section with at least 3 hyphens  
and add the lines.  
    Inline: This is an inline section  
    Inline  
    ------  
    This is a multi line inline section  
    Wow I can write multiple lines here  
    """

## Examples

### Example 1

```python
def func():
    """
    This is a function
```

## *class* **InlineParser**

> [Source: ../../miko/parsers/inline.py @ line 28-60](../../miko/parsers/inline.py#L28-L60)

An inline section parser

### *const* InlineParser.**element**

> [Source: ../../miko/parsers/inline.py @ line 30](../../miko/parsers/inline.py#L30)

### *func* InlineParser.**append**

> [Source: ../../miko/parsers/inline.py @ line 33-35](../../miko/parsers/inline.py#L33-L35)

Extends the current 

#### Parameters

- **content**: str


### *func* InlineParser.**dumps**

> [Source: ../../miko/parsers/inline.py @ line 37-57](../../miko/parsers/inline.py#L37-L57)

#### Parameters

- **indent**: int
  - Default Value: `4`


### *func* InlineParser.**__repr__**

> [Source: ../../miko/parsers/inline.py @ line 59-60](../../miko/parsers/inline.py#L59-L60)

#### Returns

- str
    - 
