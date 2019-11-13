from .compat import iteritems
from .const import Symbols
from .matcher import Matcher
from .utils import split_netloc, sub_pieces


class DictMatcher(Matcher):
    def __init__(self):
        self._rules = {}

    def match(self, netloc):
        domain, port = split_netloc(netloc)
        best_match = None
        for piece in sub_pieces(domain):
            match, rule, match_port = self._match(piece, port)
            if not match:
                continue
            if port is not None:
                if match_port:
                    return rule
                if best_match is None:
                    best_match = (rule,)
            else:
                return rule

        return best_match[0] if best_match else best_match

    def _match(self, piece, port):
        if piece not in self._rules:
            return False, None, False
        rules = self._rules[piece]
        if isinstance(rules, tuple):
            if port is not None:
                if port == rules[0]:
                    return True, rules[1], True
            if rules[0] is None:
                return True, rules[1], False
        else:
            if port is not None:
                if port in rules:
                    return True, rules[port], True
            if None in rules:
                return True, rules[None], False

        return False, None, False

    def load(self, netloc, rule, cmp=None):
        domain, port = split_netloc(netloc)
        if domain not in self._rules:
            self._rules[domain] = (port, rule)
        else:
            rules = self._rules[domain]
            if isinstance(rules, tuple):
                if port == rules[0]:
                    if cmp is not None and rule != rules[1]:
                        rule = cmp(rules[1], rule)
                    self._rules[domain] = (port, rule)
                else:
                    self._rules[domain] = dict((rules, (port, rule)))
            else:
                if port not in rules:
                    rules[port] = rule
                else:
                    if cmp is not None and rule != rules[port]:
                        rule = cmp(rules[port], rule)
                    rules[port] = rule

    def delete(self, netloc):
        domain, port = split_netloc(netloc)
        if domain not in self._rules:
            return False, None

        rules = self._rules[domain]

        if isinstance(rules, tuple):
            if port is not None:
                if port == rules[0]:
                    self._rules.pop(domain)
                    return True, rules[1]
            elif rules[0] is None:
                self._rules.pop(domain)
                return True, rules[1]
        else:
            if port is not None:
                if port in rules:
                    rule = rules.pop(port)
                    num = len(rules)
                    if num == 1:
                        self._rules[domain] = list(iteritems(rules))[0]
                    elif num == 0:
                        self._rules.pop(domain)
                    return True, rule
            elif None in rules:
                rule = rules.pop(None)
                num = len(rules)
                if num == 1:
                    self._rules[domain] = list(iteritems(rules))[0]
                elif num == 0:
                    self._rules.pop(domain)
                return True, rule

        return False, None

    def dump(self):
        for domain, rules in iteritems(self._rules):
            if isinstance(rules, tuple):
                if rules[0] is None:
                    yield domain, rules[1]
                else:
                    yield Symbols.COLON.join((domain, rules[0])), rules[1]
            else:
                for port, rule in iteritems(rules):
                    if port is None:
                        yield domain, rule
                    else:
                        yield Symbols.COLON.join((domain, port)), rule
