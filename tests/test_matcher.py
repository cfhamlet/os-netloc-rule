import pytest
from os_netloc_rule.matcher import Matcher


@pytest.fixture(scope="function")
def matcher():
    return Matcher()


def load_and_match(matcher, rules, cases):
    for domain_with_port, rule, cmp in rules:
        matcher.load(domain_with_port, rule, cmp=cmp)

    for domain_with_port, expected in cases:
        assert matcher.match(domain_with_port) == expected


def test_matcher_001(matcher):
    rules = []
    cases = []

    load_and_match(matcher, rules, cases)
