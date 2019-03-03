# rxe: literate and composable regular expressions

### Contents

- [Introduction](#introduction)
- [Motivation](#motivation)
- [Install](#install)
- [Docs](#docs)
- [Todos](#todos)

### Introduction

`rxe` is a thin wrapper around Python's `re` module (see [official re docs](https://docs.python.org/2/library/re.html)). The various `rxe` functions are wrappers around corresponding `re` patterns. For example, `rxe.digit().one_or_more('a').whitespace()` corresponds to `\da+\s`. Because `rxe` uses parentheses but wants to avoid unnamed groups, the internal (equivalent) representation is actually `\d(?:a)+\s`. This pattern can always be retrieved with `get_pattern()`.

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

Note how rxe allows the `decimal` regex to be re-used in the `coord` pattern! Although it's more code, it's much more readable.

Suppose you want to support arbitrary number of whitespace. The diff for this change will be:

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

Okay, but we also want to extract the latitude and longitude, not just match on it. Let's extract them, but in a readable way:

```python
coord = (rxe
  .literal('(')
  .zero_or_more(rxe.whitespace())
  .exactly(1, rxe.named('lat', decimal)) # <--- line changed
  .zero_or_more(rxe.whitespace())
  .literal(',')
  .zero_or_more(rxe.whitespace())
  .exactly(1, rxe.named('lon', decimal)) # <--- line changed
  .zero_or_more(rxe.whitespace())
  .literal(')')
)

m = coord.match('(23.34, 11.0)')
print(m.group('lat'))
print(m.group('lon'))
```

One more example, parsing email addresses. The regex is `[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}`. The equivalent `rxe` code:

```
username = rxe.one_or_more(rxe.set([rxe.alphanumeric(), '.', '%', '+', '-']))
domain = rxe.one_or_more(rxe.set([rxe.alphanumeric(), '.', '-']))
tld = rxe.at_least_at_most(2, 6, rxe.set([rxe.range('a', 'z'), rxe.range('A', 'Z')]))
email = (rxe
	.exactly(username)
	.literal('@')
	.exactly(domain)
	.literal('.')
	.exactly(tld)
)
```

## Install

Use `pip`:

```pip install git+git://github.com/mtrencseni/rxe```

Then:

```
$ python
>>> from rxe import *
>>> r = rxe.digit().at_least(1, 'p').at_least(2, 'q')
>>> assert(r.match('1ppppqqqqq') is not None) 
```

### Docs

Most of these functions correspond to [patterns of functions](https://docs.python.org/2/library/re.html) from `re`.

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

`range(fr, to)`: Matches the characters in the range from `fr` to `to`, like `a-z` or `0-9`.

`at_least(n, s)`: Matches if `s` occurs at least `n` times. `s` can be a literal or an `rxe` object.

`exactly(n, s)`: Matches if `s` occurs exactly `n` times. `s` can be a literal or an `rxe` object.

`one(s)`: Shorthand for `exactly(n=1, s)`.

`at_least_at_most(min, max, s)`: Matches if `s` occurs at least `min`, at most `max` times. `s` can be a literal or an `rxe` object.

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

`fullmatch(s)`: `True` if the pattern matches `s`, and consumes all of `s`.

`compile(flags=0)`: Compile a regular expression pattern into a regular expression object, which can be used for matching using its `match()` and `search()` methods. [See re docs](https://docs.python.org/2/library/re.html).

`search(string, flags=0)`: Scan through `string` looking for the first location where the regular expression pattern produces a match, and return a corresponding `MatchObject` instance. Return `None` if no position in the string matches the pattern; note that this is different from finding a zero-length match at some point in the string. [See re docs](https://docs.python.org/2/library/re.html).

`match(string, flags=0)`: If zero or more characters at the beginning of string match the regular expression pattern, return a corresponding `MatchObject` instance. Return `None` if the string does not match the pattern; note that this is different from a zero-length match. [See re docs](https://docs.python.org/2/library/re.html).

`split(string, maxsplit=0, flags=0)`: Split string by the occurrences of pattern. If capturing parentheses are used in pattern, then the text of all groups in the pattern are also returned as part of the resulting list. If `maxsplit` is nonzero, at most `maxsplit` splits occur, and the remainder of the string is returned as the final element of the list. [See re docs](https://docs.python.org/2/library/re.html).

`findall(string, flags=0)`: Return all non-overlapping matches of pattern in string, as a list of strings. The string is scanned left-to-right, and matches are returned in the order found. If one or more groups are present in the pattern, return a list of groups; this will be a list of tuples if the pattern has more than one group. Empty matches are included in the result. [See re docs](https://docs.python.org/2/library/re.html).

`finditer(string, flags=0)`: Return an iterator yielding `MatchObject` instances over all non-overlapping matches for the pattern in string. The string is scanned left-to-right, and matches are returned in the order found. Empty matches are included in the result. [See re docs](https://docs.python.org/2/library/re.html).

`sub(repl, string, count=0, flags=0)`: Return the string obtained by replacing the leftmost non-overlapping occurrences of pattern in string by the replacement `repl`. [See re docs](https://docs.python.org/2/library/re.html).

`subn(repl, string, count=0, flags=0)`: Perform the same operation as `sub()`, but return a tuple `(new_string, number_of_subs_made)`. [See re docs](https://docs.python.org/2/library/re.html).

### Todos

- write more tests
