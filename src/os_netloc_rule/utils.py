from __future__ import unicode_literals

from .const import DEFAULT_PORT, Symbols


def split_netloc(netloc, schema=None):
    last_char = ord(netloc[-1])
    if not (last_char >= 48 and last_char <= 57):
        if schema and schema in DEFAULT_PORT:
            return netloc, DEFAULT_PORT[schema]
        return netloc, None

    domain = netloc
    port = None
    t = netloc.rfind(Symbols.COLON, -6, -1)
    if t > 0:
        domain = netloc[:t]
        port = netloc[t + 1 :]

    if port is None and schema:
        if schema in DEFAULT_PORT:
            port = DEFAULT_PORT[schema]
    return domain, port


def sub_pieces(domain):
    yield domain
    idx = domain.find(Symbols.DOT)
    while idx > 0:
        yield domain[idx:]
        idx += 1
        while domain[idx] == Symbols.DOT:
            idx += 1
        yield domain[idx:]
        idx = domain.find(Symbols.DOT, idx)
