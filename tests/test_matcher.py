import pytest

from os_netloc_rule.matcher import Matcher


@pytest.fixture(scope="function")
def matcher():
    return Matcher()


def load_and_match(matcher, rules, cases):
    for rule in rules:
        matcher.load(*rule)

    for domain_with_port, expected in cases:
        assert matcher.match(domain_with_port) == expected


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
        ("www.example.com", 2, None, cmp),
        ("www.example.com", 1, None, cmp),
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
