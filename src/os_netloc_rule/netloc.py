from __future__ import unicode_literals

import operator
import sys
from collections import namedtuple

_PY3 = sys.version_info[0] >= 3

if _PY3:
    iteritems = operator.methodcaller("items")
    from urllib.parse import urlparse  # isort: skip
else:
    iteritems = operator.methodcaller("iteritems")
    from urlparse import urlparse  # isort: skip


DEFAULT_ENCODING = "UTF-8"


class Symbols(object):
    EMPTY = ""
    DOT = "."
    COLON = ":"
    VBAR = "|"


DEFAULT_PORT = {"http": "80", "https": "443", "ssh": "22", "ftp": "21"}


def sub_pieces(piece):
    yield piece
    idx = piece.find(Symbols.DOT)
    while idx > 0:
        yield piece[idx:]
        idx += 1
        while piece[idx] == Symbols.DOT:
            idx += 1
        yield piece[idx:]
        idx = piece.find(Symbols.DOT, idx)


class Netloc(namedtuple("Netloc", "host port scheme")):
    def __str__(self):
        return Symbols.VBAR.join(self)

    @staticmethod
    def from_string(s):
        c = s.split(Symbols.VBAR)
        assert len(c) == 3, "invalid netloc string host|port|scheme %s" % s
        return Netloc(host=c[0], port=c[1], scheme=c[2])


class MatchUnit(object):

    __slots__ = ["nlc_rules"]

    def __init__(self):
        self.nlc_rules = {}

    def add(self, netloc, rule, cmp=None):
        port = netloc.port
        if port not in self.nlc_rules:
            self.nlc_rules[port] = [(netloc, rule)]
            return None, None
        nlc_rules = self.nlc_rules[port]
        for i in range(0, len(nlc_rules)):
            n, r = nlc_rules[i]
            if n.scheme != netloc.scheme:
                continue
            if cmp is None or cmp(r, rule) < 0:
                nlc_rules[i] = (netloc, rule)
                return n, r
            return netloc, rule

        nlc_rules.append((netloc, rule))
        return None, None


def better_match(n1, n2, port, scheme):
    if n1[0] is None:
        return n2
    elif n2[0] is None:
        return n1

    if port:
        if n1[0].port == n2[0].port and n1[0].port == port:
            if len(n1[0].host) > len(n2[0].host):
                return n1
            return n2
        if port == n2[0].port:
            return n2
        elif port == n1[0].port:
            return n1

    if scheme:
        if n1[0].scheme == n2[0].scheme and n1[0].scheme == scheme:
            if len(n1[0].host) > len(n2[0].host):
                return n1
            return n2
        if scheme == n2[0].scheme:
            return n2
        elif scheme == n1[0].scheme:
            return n1

    if len(n2[0].host) > len(n1[0].host):
        return n2

    return n1


class Matcher(object):
    def __init__(self):
        self._size = 0
        self.units = {}

    def match_url(self, url, literal=True):
        scheme, host_with_port, _, _, _ = urlparse(url)
        c = host_with_port.split(Symbols.COLON)
        host = host_with_port
        port = ""
        if c == 1:
            if not literal and scheme and scheme in DEFAULT_PORT:
                port = DEFAULT_PORT[scheme]
        elif c == 2:
            host = c[0]
            port = c[1]
        return self.match(host, port, scheme)

    def match(self, host, port="", scheme=""):
        best = (None, None)
        for piece in sub_pieces(host):
            nlr, exact = self._match(piece, port, scheme)
            if exact:
                best = nlr
                break
            else:
                best = better_match(best, nlr, port, scheme)
        return best

    def _match(self, host, port, scheme):
        best = (None, None)
        if host not in self.units:
            return best, False
        unit = self.units[host]
        if port and port in unit.nlc_rules:
            nlrs = unit.nlc_rules[port]
            for nlr in nlrs:
                if scheme and nlr[0].scheme == scheme:
                    return nlr, True
                elif nlr[0].scheme == scheme or not nlr[0].scheme:
                    best = better_match(best, nlr, port, scheme)

        if Symbols.EMPTY in unit.nlc_rules:
            nlrs = unit.nlc_rules[Symbols.EMPTY]
            for nlr in nlrs:
                if nlr[0].scheme == scheme or not nlr[0].scheme:
                    best = better_match(best, nlr, port, scheme)

        return best, False

    def load_from_string(self, netloc_string, rule, cmp=None):
        netloc = Netloc.from_string(netloc_string)
        return self.load_from_netloc(netloc, rule, cmp)

    def load_from_netloc(self, netloc, rule, cmp=None):
        host = netloc.host
        if host not in self.units:
            self.units[host] = MatchUnit()
        n, v = self.units[host].add(netloc, rule, cmp)
        if n is None:
            self._size += 1
        return n, v

    def load(self, host, port, scheme, rule, cmp=None):
        return self.load_from_netloc(Netloc(host, port, scheme), rule, cmp)

    def delete(self, netloc):
        host = netloc.host
        if host not in self.units:
            return None, None
        unit = self.units[host]
        port = netloc.port
        if port not in unit.nlc_rules:
            return None, None
        nlrs = unit.nlc_rules[port]
        for i in range(0, len(nlrs)):
            nlr = nlrs[i]
            if nlr[0] == netloc:
                nlrs = nlrs[0:i] + nlrs[i + 1 :]
                if not nlrs:
                    unit.nlc_rules.pop(port)
                    if not unit.nlc_rules:
                        self.units.pop(host)
                self._size += -1
                return nlr
        return None, None

    def iter(self):
        for unit in self.units.values():
            for nlrs in unit.nlc_rules.values():
                for nlr in nlrs:
                    yield nlr

    def get(self, netloc):
        host = netloc.host
        if host not in self.units:
            return None, None
        unit = self.units[host]
        if netloc.port not in unit.nlc_rules:
            return None, None
        nlrs = unit.nlc_rules[netloc.port]
        for nlc, rule in nlrs:
            if nlc == netloc:
                return nlc, rule
        return None, None

    def size(self):
        return self._size
