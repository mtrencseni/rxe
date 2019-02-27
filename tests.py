
import re
import rxe

def test_rxe():
    r = rxe.digit().min(n=1, s='p').min(n=2, s='q')
    assert(r.match('1ppppqqqqq') is not None)
    assert(r.match('pqq') is None)
    assert(r.match('3hello') is None)

    r = (rxe.literal('(').zero_or_more(rxe.alphanumeric()).literal(')').zero_or_one('hello'))
    assert(r.match('(43453453)sdsd') is not None)
    assert(r.fullmatch('(43453453)sdsd') is None)
    assert(r.fullmatch('(43453453)') is not None)
    assert(r.fullmatch('(43453453)hello') is not None)
    assert(r.fullmatch('(43453453)helloZ') is None)

    decimal_expr = (rxe
        .min(1, rxe.digit())
        .literal('.')
        .min(1, rxe.digit())
        )
    int_expr = (rxe
        .min(1, rxe.digit())
        )
    number = rxe.either(decimal_expr, int_expr)
    assert(number.fullmatch('hello') is None)
    assert(number.fullmatch('12323') is not None)
    assert(number.fullmatch('0.984') is not None)
    assert(number.fullmatch('0') is not None)
    assert(number.fullmatch('0.') is None)

    r = (rxe.literal('x').named('middle', rxe.set(['a', 'b', 'c', rxe.digit()])).literal('y'))
    assert(r.fullmatch('xay') is not None)
    assert(r.fullmatch('xby') is not None)
    assert(r.fullmatch('xcy') is not None)
    assert(r.fullmatch('x1y') is not None)
    assert(r.fullmatch('xy') is None)
    assert(r.fullmatch('x11y') is None)
    assert(r.fullmatch('xaay') is None)
    assert(r.fullmatch('hello') is None)
    assert(r.fullmatch('x1y').group('middle') == '1')

    decimal = (rxe.one_or_more(rxe.digit()).literal('.').one_or_more(rxe.digit()))
    coord = (rxe.literal('(').exactly(1, decimal).literal(',').exactly(1, decimal).literal(')'))
    assert(coord.fullmatch('hello') is None)
    assert(coord.fullmatch('(23.34,11.0)') is not None)
    assert(coord.fullmatch('(23.34, 11.0)') is None)
    coord = (rxe
      .literal('(')
      .zero_or_more(rxe.whitespace()) # <--- line added
      .exactly(1, rxe.named('lat', decimal))
      .zero_or_more(rxe.whitespace()) # <--- line added
      .literal(',')
      .zero_or_more(rxe.whitespace()) # <--- line added
      .exactly(1, rxe.named('lon', decimal))
      .zero_or_more(rxe.whitespace()) # <--- line added
      .literal(')')
    )
    assert(coord.fullmatch('hello') is None)
    assert(coord.fullmatch('(23.34,11.0)') is not None)
    assert(coord.fullmatch('(23.34, 11.0)') is not None)
    assert(coord.fullmatch('(    23.34  , 11.0  )') is not None)
    m = coord.match('(23.34, 11.0)')
    assert(m.group('lat') == '23.34')
    assert(m.group('lon') == '11.0')
