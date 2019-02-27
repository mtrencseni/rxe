
import re
import rxe

# r1 = (rxe
#     .digit()
#     .min(n=1, s='p')
#     .min(n=2, s='q')
#     )

# print(r1.match('1ppppqqqqq'))
# print(r1.match('pqq'))
# print(r1.match('3hello'))

# r2 = (rxe
#     .literal('(')
#     .zero_or_more(rxe.alphanumeric())
#     .literal(')')
#     .zero_or_one('hello')
#     )

# print(r2.match('(43453453)sdsd'))
# print(r2.fullmatch('(43453453)sdsd'))
# print(r2.fullmatch('(43453453)'))
# print(r2.fullmatch('(43453453)hello'))
# print(r2.fullmatch('(43453453)helloZ'))

# decimal_expr = (rxe
#     .min(1, rxe.digit())
#     .literal('.')
#     .min(1, rxe.digit())
#     )

# int_expr = (rxe
#     .min(1, rxe.digit())
#     )

# number = rxe.either(decimal_expr, int_expr)

# print(number.fullmatch('hello'))
# print(number.fullmatch('12323'))
# print(number.fullmatch('0.984'))
# print(number.fullmatch('0'))
# print(number.fullmatch('0.'))

r3 = (rxe
    .literal('x')
    .named('middle', rxe.set(['a', 'b', 'c', rxe.digit()]))
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
