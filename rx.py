import re

class rx:
    def __init__(self):
        self.regex = ''
    
    def raw(self, regex):
        self.regex += regex
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
    
    def whitepspace(self):
        return self.raw('\s')
    
    def non_whitespace(self):
        return self.raw('\S')
    
    def word_boundary(self):
        return self.raw('\b')

    def non_word_boundary(self):
        return self.raw('\B')

    def literal(self, s):
        s = re.escape(s)
        self.regex += s
        return self
    
    @staticmethod
    def to_regexp_str(s):
        if type(s) is str:
            return re.escape(s)
        elif type(s) is type(rx()):
            return s.regex
        return s
    
    def min(self, n, s):
        s = rx.to_regexp_str(s)
        parens = '(?:' + s + ')'
        if n == 0:
            self.regex += parens + '*'
        elif n == 1:
            self.regex += parens + '+'
        else:
            self.regex += parens + '{%d,}' % n
        return self
    
    def exactly(self, n, s):
        s = rx.to_regexp_str(s)
        parens = '(?:' + s + ')'
        self.regex += parens + '{%d}' % n
        return self

    def minmax(self, min, max, s):
        s = rx.to_regexp_str(s)
        parens = '(?:' + s + ')'
        if min == 0 and max == 1:
            self.regex += parens + '?'
        else:
            self.regex += parens + '{%d,%d}' % (min, max)
        return self
    
    def zero_or_more(self, s):
        return self.min(0, s)
    
    def at_least_one(self, s):
        return self.min(1, s)
    
    def zero_or_one(self, s):
        return self.minmax(0, 1, s)
    
    def non_greedy(self):
        return self.raw('?')
    
    def either(self, s1, s2):
        s1 = rx.to_regexp_str(s1)
        s2 = rx.to_regexp_str(s2)
        parens1 = '(?:' + s1 + ')'
        parens2 = '(?:' + s2 + ')'
        self.regex += parens1 + '|' + parens2
        return self
    
    def set(self, li):
        s = ''.join([rx.to_regexp_str(i) for i in li])
        self.regex += '[' + s + ']'
        return self

    def non_named(self, name, s):
        s = rx.to_regexp_str(s)
        self.regex += '(' + s + ')'
        return self
    
    def named(self, name, s):
        s = rx.to_regexp_str(s)
        self.regex += '(?P<%s>%s)' % (name, s)
        return self
    
    def assert_lookahead(self, s):
        s = rx.to_regexp_str(s)
        self.regex += '(?=' + s + ')'
        return self
    
    def assert_lookahead_not(self, s):
        s = rx.to_regexp_str(s)
        self.regex += '(?!' + s + ')'
        return self
    
    def expr(self):
        return self.regex

    def fullmatch(self, s):
        m = re.compile(self.regex + '$')
        return m.match(s)
    
    def compile(self, flags=0):
        return re.compile(self.regex, flags)

    def search(self, string, flags=0):
        return re.search(self.regex, string, flags)
    
    def match(self, string, flags=0):
        return re.match(self.regex, string, flags)

    def split(self, string, maxsplit=0, flags=0):
        return re.split(self.regex, string, maxsplit, flags)

    def findall(self, string, flags=0):
        return re.findall(self.regex, string, flags)
    
    def finditer(self, string, flags=0):
        return re.finditer(self.regex, string, flags)
    
    def sub(self, repl, string, count=0, flags=0):
        return re.sub(self.regex, repl, string, count=0, flags=0)

    def subn(self, repl, string, count=0, flags=0):
        return re.subn(self.regex, repl, string, count=0, flags=0)
    
def digit():
    return rx().digit()
    
def alphanumeric():
    return rx().alphanumeric()

def literal(s):
    return rx().literal(s)

def min(n, s):
    return rx().min(n, s)

def either(s1, s2):
    return rx().either(s1, s2)

def set(li):
    return rx().set(li)

