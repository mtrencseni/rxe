
import re
import rx

# r1 = (rx
#     .digit()
#     .min(n=1, s='p')
#     .min(n=2, s='q')
#     )

# print(r1.match('1ppppqqqqq'))
# print(r1.match('pqq'))
# print(r1.match('3hello'))

# r2 = (rx
#     .literal('(')
#     .zero_or_more(rx.alphanumeric())
#     .literal(')')
#     .zero_or_one('hello')
#     )

# print(r2.match('(43453453)sdsd'))
# print(r2.fullmatch('(43453453)sdsd'))
# print(r2.fullmatch('(43453453)'))
# print(r2.fullmatch('(43453453)hello'))
# print(r2.fullmatch('(43453453)helloZ'))

# decimal_expr = (rx
#     .min(1, rx.digit())
#     .literal('.')
#     .min(1, rx.digit())
#     )

# int_expr = (rx
#     .min(1, rx.digit())
#     )

# number = rx.either(decimal_expr, int_expr)

# print(number.fullmatch('hello'))
# print(number.fullmatch('12323'))
# print(number.fullmatch('0.984'))
# print(number.fullmatch('0'))
# print(number.fullmatch('0.'))

r3 = (rx
    .literal('x')
    .named('middle', rx.set(['a', 'b', 'c', rx.digit()]))
    .literal('y')
    )
print(r3.fullmatch('xay'))
print(r3.fullmatch('xby'))
print(r3.fullmatch('xcy'))
print(r3.fullmatch('x1y'))
print(r3.fullmatch('xy'))
print(r3.fullmatch('x11y'))
print(r3.fullmatch('xaay'))
print(r3.fullmatch('hello'))
print(r3.fullmatch('x1y').group('middle'))

