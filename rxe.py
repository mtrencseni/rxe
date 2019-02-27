import re

class rxe:
    def __init__(self):
        self.pattern = ''
    
    def raw(self, pattern):
        self.pattern += pattern
        return self

    def any_character(self):
        return self.raw('.')

    def begin_line(self):
        return self.raw('^')
    
    def end_line(self):
        return self.raw('$')
    
    def begin_string(self):
        return self.raw('\A')
    
    def end_string(self):
        return self.raw('\Z')

    def digit(self):
        return self.raw('\d')
    
    def non_digit(self):
        return self.raw('\D')

    def alphanumeric(self):
        return self.raw('\w')

    def non_alphanumeric(self):
        return self.raw('\W')
    
    def whitespace(self):
        return self.raw('\s')
    
    def non_whitespace(self):
        return self.raw('\S')
    
    def word_boundary(self):
        return self.raw('\b')

    def non_word_boundary(self):
        return self.raw('\B')

    def literal(self, s):
        s = re.escape(s)
        self.pattern += s
        return self
    
    @staticmethod
    def to_regexp_str(s):
        if type(s) is str:
            return re.escape(s)
        elif type(s) is type(rxe()):
            return s.pattern
        return s
    
    def min(self, n, s):
        s = rxe.to_regexp_str(s)
        parens = '(?:' + s + ')'
        if n == 0:
            self.pattern += parens + '*'
        elif n == 1:
            self.pattern += parens + '+'
        else:
            self.pattern += parens + '{%d,}' % n
        return self
    
    def exactly(self, n, s):
        s = rxe.to_regexp_str(s)
        parens = '(?:' + s + ')'
        self.pattern += parens + '{%d}' % n
        return self

    def minmax(self, min, max, s):
        s = rxe.to_regexp_str(s)
        parens = '(?:' + s + ')'
        if min == 0 and max == 1:
            self.pattern += parens + '?'
        else:
            self.pattern += parens + '{%d,%d}' % (min, max)
        return self
    
    def zero_or_more(self, s):
        return self.min(0, s)
    
    def one_or_more(self, s):
        return self.min(1, s)
    
    def zero_or_one(self, s):
        return self.minmax(0, 1, s)
    
    def non_greedy(self):
        return self.raw('?')
    
    def either(self, s1, s2):
        s1 = rxe.to_regexp_str(s1)
        s2 = rxe.to_regexp_str(s2)
        parens1 = '(?:' + s1 + ')'
        parens2 = '(?:' + s2 + ')'
        self.pattern += parens1 + '|' + parens2
        return self
    
    def set(self, li):
        s = ''.join([rxe.to_regexp_str(i) for i in li])
        self.pattern += '[' + s + ']'
        return self

    def non_named(self, name, s):
        s = rxe.to_regexp_str(s)
        self.pattern += '(' + s + ')'
        return self
    
    def named(self, name, s):
        s = rxe.to_regexp_str(s)
        self.pattern += '(?P<%s>%s)' % (name, s)
        return self
    
    def assert_lookahead(self, s):
        s = rxe.to_regexp_str(s)
        self.pattern += '(?=' + s + ')'
        return self
    
    def assert_lookahead_not(self, s):
        s = rxe.to_regexp_str(s)
        self.pattern += '(?!' + s + ')'
        return self
    
    def get_pattern(self):
        return self.pattern

    def fullmatch(self, s):
        m = re.compile(self.pattern + '$')
        return m.match(s)
    
    def compile(self, flags=0):
        return re.compile(self.pattern, flags)

    def search(self, string, flags=0):
        return re.search(self.pattern, string, flags)
    
    def match(self, string, flags=0):
        return re.match(self.pattern, string, flags)

    def split(self, string, maxsplit=0, flags=0):
        return re.split(self.pattern, string, maxsplit, flags)

    def findall(self, string, flags=0):
        return re.findall(self.pattern, string, flags)
    
    def finditer(self, string, flags=0):
        return re.finditer(self.pattern, string, flags)
    
    def sub(self, repl, string, count=0, flags=0):
        return re.sub(self.pattern, repl, string, count=0, flags=0)

    def subn(self, repl, string, count=0, flags=0):
        return re.subn(self.pattern, repl, string, count=0, flags=0)

def raw(pattern):
    return rxe().raw(pattern)

def any_character():
    return rxe().any_character()

def begin_line():
    return rxe().begin_line()

def end_line():
    return rxe().end_line()

def begin_string():
    return rxe().begin_string()

def end_string():
    return rxe().end_string()

def digit():
    return rxe().digit()

def non_digit():
    return rxe().non_digit()

def alphanumeric():
    return rxe().alphanumeric()

def non_alphanumeric():
    return rxe().non_alphanumeric()

def whitespace():
    return rxe().whitespace()

def non_whitespace():
    return rxe().non_whitespace()

def word_boundary():
    return rxe().word_boundary()

def non_word_boundary():
    return rxe().non_word_boundary()

def literal(s):
    return rxe().literal(s)

def min(n, s):
    return rxe().min(n, s)

def exactly(n, s):
    return rxe().exactly(n, s)

def minmax(min, max, s):
    return rxe().minmax(min, max, s)

def zero_or_more(s):
    return rxe().zero_or_more(s)

def one_or_more(s):
    return rxe().one_or_more(s)

def zero_or_one(s):
    return rxe().zero_or_one(s)

def non_greedy():
    return rxe().non_greedy()

def either(s1, s2):
    return rxe().either(s1, s2)

def set(li):
    return rxe().set(li)

def non_named(name, s):
    return rxe().non_named(name, s)

def named(name, s):
    return rxe().named(name, s)

def assert_lookahead(s):
    return rxe().assert_lookahead(s)

def assert_lookahead_not(s):
    return rxe().assert_lookahead_not(s)
