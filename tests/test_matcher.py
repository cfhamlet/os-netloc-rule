import pytest

from os_netloc_rule import DictMatcher, TreeMatcher


@pytest.fixture(scope="function", params=[TreeMatcher, DictMatcher])
def matcher(request):
    return request.param()


def load_and_match(matcher, rules, cases):
    for rule in rules:
        matcher.load(*rule)

    for netloc, expected in cases:
        assert matcher.match(netloc) == expected


def test_matcher_001(matcher):
    rules = [
        ("www.example.com", 1),
        ("example.com", 2),
        ("example.com:88", 3),
        ("test.com", 4),
    ]
    cases = [
        ("www.example.com", 1),
        ("abc.example.com", 2),
        ("123.example.com:88", 3),
        ("test.com:88", 4),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_002(matcher):
    rules = [
        (".example.com", 1),
        ("example.com", 2),
    ]
    cases = [
        ("www.example.com", 1),
        ("example.com", 2),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_003(matcher):
    rules = [
        ("www.example.com", 1),
        ("www.example.com", 2),
    ]
    cases = [
        ("www.example.com", 2),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_003(matcher):
    def cmp(x, y):
        return x if x > y else y

    rules = [
        ("www.example.com", 2, cmp),
        ("www.example.com", 1, cmp),
    ]
    cases = [
        ("www.example.com", 2),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_004(matcher):
    rules = [
        ("www.example.com", 1),
        ("abc.example.com", 2),
        (".example.com:8080", 3),
    ]
    cases = [
        ("www.example.com", 1),
        ("abc.example.com", 2),
        ("abc.example.com:8080", 3),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_005(matcher):
    rules = [
        ("www.example.com:80", 1),
        ("www.example.com:80", 2),
    ]
    cases = [
        ("www.example.com:80", 2),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_006(matcher):
    rules = [
        ("www.example.com:80", 1),
        ("www.example.com:8080", 2),
    ]
    cases = [
        ("www.example.com:70", None),
        ("www.example.com:80", 1),
        ("www.example.com:8080", 2),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_007(matcher):
    rules = [
        ("www.example.com", 1),
        ("www.example.com:8080", 2),
    ]
    cases = [
        ("www.example.com:70", 1),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_008(matcher):
    rules = [
        (".example.com", 1),
        ("abc.example.com", None),
        ("123.abc.example.com", 3),
    ]
    cases = [
        ("1.abc.example.com", None),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_009(matcher):
    def cmp(x, y):
        return x if x > y else y

    rules = [
        ("www.example.com:80", 2, cmp),
        ("www.example.com:90", 1, cmp),
    ]
    cases = [
        ("www.example.com:80", 2),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_010(matcher):
    def cmp(x, y):
        return x if x > y else y

    rules = [
        ("www.example.com:80", 3, cmp),
        ("www.example.com:80", 2, cmp),
        ("www.example.com:80", 1, cmp),
    ]
    cases = [
        ("www.example.com:80", 3),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_011(matcher):

    rules = [
        ("www.example.com:80", 3),
        ("www.example.com:80", 2),
        ("www.example.com:80", 1),
    ]
    cases = [
        ("www.example.com:80", 1),
    ]

    load_and_match(matcher, rules, cases)


def test_matcher_dump_001(matcher):
    rules = [
        ("www.example.com:80", 1),
        ("www.example.com:8080", 2),
        (".example.com:8080", 3),
        (".example.com", 4),
    ]

    for domain_with_port, rule in rules:
        matcher.load(domain_with_port, rule)

    o = list(matcher.dump())

    assert set(o) == set(rules)


def test_matcher_dump_002(matcher):
    rules = [
        ("www.example.com", 1),
        ("www.example.com:80", 2),
    ]

    for domain_with_port, rule in rules:
        matcher.load(domain_with_port, rule)

    o = list(matcher.dump())

    assert set(o) == set(rules)


def test_matcher_delete_001(matcher):
    rules = [
        ("www.example.com:80", 1),
    ]

    for domain_with_port, rule in rules:
        matcher.load(domain_with_port, rule)

    assert matcher.delete("www.example.com") == (False, None)
    assert matcher.delete("www.example.com:80") == (True, 1)

    o = list(matcher.dump())
    assert set(o) == set([])


def test_matcher_delete_002(matcher):
    rules = [
        ("www.example.com", 0),
        ("www.example.com:80", 1),
        ("www.example.com:8080", 2),
        ("abc.example.com:8080", 3),
    ]

    for domain_with_port, rule in rules:
        matcher.load(domain_with_port, rule)

    assert matcher.delete("www.example.com") == (True, 0)
    assert matcher.delete("www.example.com:80") == (True, 1)
    assert matcher.delete("www.example.com:8080") == (True, 2)
    assert matcher.delete("abc.example.com:8080") == (True, 3)

    o = list(matcher.dump())
    assert set(o) == set([])


def test_matcher_delete_003(matcher):
    rules = [
        ("www.example.com", 0),
    ]

    for domain_with_port, rule in rules:
        matcher.load(domain_with_port, rule)

    assert matcher.delete("www.test.com") == (False, None)
    assert matcher.delete("www.example.com") == (True, 0)

    o = list(matcher.dump())
    assert set(o) == set([])


def test_matcher_delete_004(matcher):
    rules = [
        ("www.example.com:80", 0),
        ("www.example.com:90", 1),
    ]

    for domain_with_port, rule in rules:
        matcher.load(domain_with_port, rule)

    assert matcher.delete("www.example.com:80") == (True, 0)
    assert matcher.delete("www.example.com:90") == (True, 1)

    o = list(matcher.dump())
    assert set(o) == set([])


def test_matcher_delete_005(matcher):
    rules = [
        ("www.example.com:80", 0),
        ("www.example.com:90", 1),
        ("www.example.com", 2),
    ]

    for domain_with_port, rule in rules:
        matcher.load(domain_with_port, rule)

    assert matcher.delete("www.example.com:80") == (True, 0)
    assert matcher.delete("www.example.com:90") == (True, 1)
    assert matcher.delete("www.example.com") == (True, 2)

    o = list(matcher.dump())
    assert set(o) == set([])
