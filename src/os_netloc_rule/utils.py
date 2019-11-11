from __future__ import unicode_literals

from .const import DEFAULT_PORT, Symbols


def split_domain_port(domain_with_port, schema=None):
    last_char = ord(domain_with_port[-1])
    if not (last_char >= 48 and last_char <= 57):
        if schema and schema in DEFAULT_PORT:
            return domain_with_port, DEFAULT_PORT[schema]
        return domain_with_port, None

    domain = domain_with_port
    port = None
    t = domain_with_port.rfind(Symbols.COLON, -6, -1)
    if t > 0:
        domain = domain_with_port[:t]
        port = domain_with_port[t + 1 :]

    if port is None and schema:
        if schema in DEFAULT_PORT:
            port = DEFAULT_PORT[schema]
    return domain, port
