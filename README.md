# rxe: literate regular expressions

### Contents

- [Introduction](#introduction)
- [Motivation](#motivation)
- [Install](#install)
- [Docs](#docs)
- [Todos](#todos)

### Introduction

`rxe` is a thin wrapper around Python's `re` module. The various `rxe` functions are wrapper around corresponding `re` patterns. For example, `rxe.digit().one_or_more('a').whitespace()` corresponds to `\da+\s`. Because `rxe` uses parentheses but wants to avoid unnamed groups, the internal (equivalent) representation is actually `\d(?:a)+\s`. This pattern can always be retrieved with `get_pattern()`.

### Motivation

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

## Install

Use `pip`:

```pip install rxe```

### Docs

`any_character()`: In the default mode, this matches any character except a newline. If the `DOTALL` flag has been specified, this matches any character including a newline.

`begin_line()`: Matches the start of the string, and in `MULTILINE` mode also matches immediately after each newline.

`end_line()`: Matches the end of the string or just before the newline at the end of the string, and in `MULTILINE` mode also matches before a newline.

`begin_string()`: Matches only at the start of the string.

`end_string()`: Matches only at the end of the string.

`digit()`: When the `UNICODE` flag is not specified, matches any decimal digit; this is equivalent to the set `[0-9]`. With `UNICODE`, it will match whatever is classified as a decimal digit in the Unicode character properties database.

`non_digit()`: When the `UNICODE` flag is not specified, matches any non-digit character; this is equivalent to the set `[^0-9]`. With `UNICODE`, it will match anything other than character marked as digits in the Unicode character properties database.

`alphanumeric()`: When the `LOCALE` and `UNICODE` flags are not specified, matches any alphanumeric character and the underscore; this is equivalent to the set `[a-zA-Z0-9_]`. With `LOCALE`, it will match the set `[0-9_]` plus whatever characters are defined as alphanumeric for the current locale. If `UNICODE` is set, this will match the characters `[0-9_]` plus whatever is classified as alphanumeric in the Unicode character properties database.

`non_alphanumeric()`: When the `LOCALE` and `UNICODE` flags are not specified, matches any non-alphanumeric character; this is equivalent to the set `[^a-zA-Z0-9_]`. With `LOCALE`, it will match any character not in the set `[0-9_]`, and not defined as alphanumeric for the current locale. If `UNICODE` is set, this will match anything other than `[0-9_]` plus characters classified as not alphanumeric in the Unicode character properties database.

`whitespace()`: When the `UNICODE` flag is not specified, it matches any whitespace character, this is equivalent to the set `[ \t\n\r\f\v]`. The `LOCALE` flag has no extra effect on matching of the space. If `UNICODE` is set, this will match the characters `[ \t\n\r\f\v]` plus whatever is classified as space in the Unicode character properties database.

`non_whitespace()`: When the `UNICODE` flag is not specified, matches any non-whitespace character; this is equivalent to the set `[^ \t\n\r\f\v]` The `LOCALE` flag has no extra effect on non-whitespace match. If `UNICODE` is set, then any character not marked as space in the Unicode character properties database is matched.

`word_boundary()`: Matches the empty string, but only at the beginning or end of a word. A word is defined as a sequence of alphanumeric or underscore characters, so the end of a word is indicated by whitespace or a non-alphanumeric, non-underscore character. 

`non_word_boundary()`: Matches the empty string, but only when it is not at the beginning or end of a word.

`literal(s)`: Matches the literal string `s`.

`min(n, s)`: Matches if `s` occurs at least `n` times. `s` can be a literal or an `rxe` object.

`exactly(n, s)`: Matches if `s` occurs exactly `n` times. `s` can be a literal or an `rxe` object.

`minmax(min, max, s)`: Matches if `s` occurs at least `min`, at most `max` times. `s` can be a literal or an `rxe` object.

`zero_or_more(s)`: Matches if `s` occurs 0 or more times. `s` can be a literal or an `rxe` object.

`one_or_more(s)`: Matches if `s` occurs 1 or more times. `s` can be a literal or an `rxe` object.

`zero_or_one(s)`: Matches if `s` occurs 0 or 1 times. `s` can be a literal or an `rxe` object.

`non_greedy(self)`: Causes the *preceding* part of the pattern to be non-greedy.

`either(s1, s2)`: Matches either `s1` or `s2`. Both `s1` and `s2` can `rxe` objects.

`set(li)`: Matches the set `li`, which can also include `rxe` objects. Example `['a', 'b', rxe.digit()]`

`named(name, s)`: Creates a named match group, see the example above.

`assert_lookahead(s)`: Matches if `s` matches next, but doesn’t consume any of the string.

`assert_lookahead_not(s)`: Matches if `s` doesn’t match next.

`get_pattern()`: Returns the underlying regular expression pattern.

`fullmatch(s)`: `True` if 

`compile(flags=0)`: todo

`search(string, flags=0)`: todo

`match(string, flags=0)`: todo

`split(string, maxsplit=0, flags=0)`: todo

`findall(string, flags=0)`: todo

`finditer(string, flags=0)`: todo

`sub(repl, string, count=0, flags=0)`: todo

`subn(repl, string, count=0, flags=0)`: todo

### Todos

- add documentation
- pip install rxe
