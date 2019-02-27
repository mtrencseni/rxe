# rxe: literate regular expressions

Suppose you want to parse geo coordinates from a string, like `(<latitude>,<longitude>)`, where each is a decimal. The raw regular expression would look like `\(\d+\.\d\+,\d+\.\d\+)`. This is hard to read and maintain for the next guy, and diffs will be hard to understand and verify.

With rx, you can write:

```python
decimal = (rxe
  .one_or_more(rxe.digit())
  .literal('.')
  .one_or_more(rxe.digit())
)
coord = (rxe
  .literal('(')
  .exactly(1, decimal)
  .literal(',')
  .exactly(1, decimal)
  .literal(')')
)
```

Although it's more code, it's much more readable. Suppose you want to support arbitrary number of whitespace. The diff for this change will be:

```python
decimal = (rxe
  .one_or_more(rxe.digit())
  .literal('.')
  .one_or_more(rxe.digit())
)
coord = (rxe
  .literal('(')
  .zero_or_more(rxe.whitespace()) # <--- line added
  .exactly(1, decimal)
  .zero_or_more(rxe.whitespace()) # <--- line added
  .literal(',')
  .zero_or_more(rxe.whitespace()) # <--- line added
  .exactly(1, decimal)
  .zero_or_more(rxe.whitespace()) # <--- line added
  .literal(')')
)
```

Todos
-----

- ability to write rxe.whitespace() instead of rxe().whitespace() for all functions
- write a lot of tests
