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

Okay, but we also want to get the latitude and longitude. Let's extract them, but in a readable way:

```python
coord = (rxe
  .literal('(')
  .zero_or_more(rxe.whitespace())
  .exactly(1, rxe.named('lat', decimal)) # <--- line changed
  .zero_or_more(rxe.whitespace())
  .literal(',')
  .zero_or_more(rxe.whitespace())
  .exactly(1, rxe.named('lat', decimal)) # <--- line changed
  .zero_or_more(rxe.whitespace())
  .literal(')')
)

m = coord2.match('(23.34, 11.0)')
print(m.group('lat'))
print(m.group('lon'))
```

Todos
-----

- write a lot of tests
- add documentation
