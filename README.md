# rx: literate regular expressions

Suppose you want to parse geo coordinates from a string, like `(<latitude>,<longitude>)`, where each is a decimal. The raw regular expression would look like `\(\d+\.\d\+,\d+\.\d\+)`. This is hard to read and maintain for the next guy, and diffs will be hard to understand and verify.

With rx, you can write:

```python
decimal = (rx
  .one_or_more(rx.digit())
  .literal('.')
  .one_or_more(rx.digit())
)
coord = (rx
  .literal('(')
  .exactly(1, decimal)
  .literal(',')
  .exactly(1, decimal)
  .literal(')')
)
```

Although it's more code, it's much more readable. Suppose you want to support arbitrary number of whitespace. The diff for this change will be much cleaner compared to changing the raw regular expression:

```python
decimal = (rx
  .one_or_more(rx.digit())
  .literal('.')
  .one_or_more(rx.digit())
)
coord = (rx
  .literal('(')
  .zero_or_more(rx.whitespace()) # line added
  .exactly(1, decimal)
  .zero_or_more(rx.whitespace()) # line added
  .literal(',')
  .zero_or_more(rx.whitespace()) # line added
  .exactly(1, decimal)
  .zero_or_more(rx.whitespace()) # line added
  .literal(')')
)
```

Todos
-----

- ability to write rx.whitespace() instead of rx().whitespace() for all functions
- write a lot of tests
