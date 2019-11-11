from .const import Symbols


class Node(object):
    __slots__ = ("_children", "_default_rule", "_port_rules")

    def __init__(self, port=None, rule=None):
        self._children = None
        self._default_rule = rule if port == -1 else None
        self._port_rules = (port, rule) if port is not None and port != -1 else None

    def add_child(self, piece, port=None, rule=None, cmp=None):
        if self._children is None:
            self._children = (piece, Node(port, rule))
            return self._children[1]

        if isinstance(self._children, tuple):
            child = self._children[1]
            if piece == self._children[0]:
                child.add_rule(port, rule, cmp)
                return child
            new_child = Node(port, rule)
            self._children = {self._children[0]: self._children[1], piece: new_child}
            return new_child

        if piece not in self._children:
            child = Node(port, rule)
            self._children[piece] = child
            return child

        child = self._children[piece]
        child.add_rule(port, rule, cmp)
        return child

    def get_rule(self, port):
        rule = match_port = None
        if self._port_rules is None:
            if self._default_rule is not None:
                rule = self._default_rule
                match_port = False
        elif isinstance(self._port_rules, tuple):
            if port == self._port_rules[0]:
                rule = self._port_rules[1]
                match_port = True
        else:
            if port in self._port_rules:
                rule = self._port_rules[port]
                match_port = True

        if rule is None and self._default_rule is not None:
            rule = self._default_rule
            match_port = False

        return rule, match_port

    def match_child(self, piece):
        wildcard = exact = None
        if self._children is not None:
            if isinstance(self._children, tuple):
                if piece == self._children[0]:
                    exact = self._children[1]
                elif self._children[0] == Symbols.EMPTY:
                    wildcard = self._children[1]
            else:
                if Symbols.EMPYT in self._children:
                    wildcard = self._children[Symbols.EMPYT]
                if piece in self._children:
                    exact = self._children[piece]
        return wildcard, exact

    def add_rule(self, port, rule, cmp=None):
        if port is None:
            return
        elif port == -1:
            if self._default_rule is not None:
                if cmp is not None:
                    rule = cmp(self._default_rule, rule)
            self._default_rule = rule
        else:
            if self._port_rules is None:
                self._port_rules = (port, rule)
            elif isinstance(self._port_rules, tuple):
                if port == self._port_rules[0]:

                    if rule != self._port_rules[1]:
                        if cmp is not None:
                            rule = cmp(self._port_rules[1], rule)
                        self._port_rules = (port, rule)
                else:
                    self._port_rules = dict((self._port_rules, (port, rule)))
            elif port not in self._port_rules:
                self._port_rules[port] = rule
            else:
                if cmp is not None:
                    rule = cmp(self._port_rules[port], rule)
                self._port_rules[port] = rule


def load_from_pieces(root, pieces, port, rule, cmp=None):

    node = root
    if len(pieces) > 1:
        node = root.add_child(pieces[-1])

    for piece in pieces[-2:0:-1]:
        node = node.add_child(piece)

    node.add_child(pieces[0], port if port is not None else -1, rule, cmp=cmp)
    return root


def match_with_pieces(root, pieces, port):

    exact = root
    best_match = (None, None)  # rule, match_port

    for piece in pieces[::-1]:
        wildcard, exact = exact.match_child(piece)
        for node in (wildcard, exact):
            if node is not None:
                rule, match_port = node.get_rule(port)
                if rule is not None:
                    if not (best_match[1] and not match_port):
                        best_match = (rule, match_port)
        if exact is None:
            break
    return best_match[0]


def load(root, domain, port, rule, cmp=None):
    return load_from_pieces(root, domain.split(Symbols.DOT), port, rule, cmp)


def match(root, domain, port):
    return match_with_pieces(domain.split(Symbols.DOT), port)
