import pytest

from os_netloc_rule import Matcher, Netloc


@pytest.fixture()
def matcher():
    return Matcher()


def load_and_match(matcher, cases, expects):
    for case in cases:
        matcher.load_from_string(*case)

    for netloc_string, expected in expects:
        assert matcher.match(*Netloc.from_string(netloc_string))[1] == expected


def test_matcher_001(matcher):
    cases = [
        ("www.example.com||", 1),
        ("example.com||", 2),
        ("example.com|88|", 3),
        ("test.com||", 4),
    ]
    expects = [
        ("www.example.com||", 1),
        ("abc.example.com||", 2),
        ("123.example.com|88|", 3),
        ("test.com|88|", 4),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_002(matcher):
    cases = [
        (".example.com||", 1),
        ("example.com||", 2),
    ]
    expects = [
        ("www.example.com||", 1),
        ("example.com||", 2),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_003(matcher):
    cases = [
        ("www.example.com||", 1),
        ("www.example.com||", 2),
    ]
    expects = [
        ("www.example.com||", 2),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_003(matcher):
    def cmp(x, y):
        return x if x > y else y

    cases = [
        ("www.example.com||", 2, cmp),
        ("www.example.com||", 1, cmp),
    ]
    expects = [
        ("www.example.com||", 2),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_004(matcher):
    cases = [
        ("www.example.com||", 1),
        ("abc.example.com||", 2),
        (".example.com|8080|", 3),
    ]
    expects = [
        ("www.example.com||", 1),
        ("abc.example.com||", 2),
        ("abc.example.com|8080|", 3),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_005(matcher):
    cases = [
        ("www.example.com|80|", 1),
        ("www.example.com|80|", 2),
    ]
    expects = [
        ("www.example.com|80|", 2),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_006(matcher):
    cases = [
        ("www.example.com|80|", 1),
        ("www.example.com|8080|", 2),
    ]
    expects = [
        ("www.example.com|70|", None),
        ("www.example.com|80|", 1),
        ("www.example.com|8080|", 2),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_007(matcher):
    cases = [
        ("www.example.com||", 1),
        ("www.example.com|8080|", 2),
    ]
    expects = [
        ("www.example.com|70|", 1),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_008(matcher):
    cases = [
        (".example.com||", 1),
        ("abc.example.com||", None),
        ("123.abc.example.com||", 3),
    ]
    expects = [
        ("1.abc.example.com||", None),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_009(matcher):
    def cmp(x, y):
        return x if x > y else y

    cases = [
        ("www.example.com|80|", 2, cmp),
        ("www.example.com|90|", 1, cmp),
    ]
    expects = [
        ("www.example.com|80|", 2),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_010(matcher):
    def cmp(x, y):
        return x if x > y else y

    cases = [
        ("www.example.com|80|", 3, cmp),
        ("www.example.com|80|", 2, cmp),
        ("www.example.com|80|", 1, cmp),
    ]
    expects = [
        ("www.example.com|80|", 3),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_011(matcher):

    cases = [
        ("www.example.com|80|", 3),
        ("www.example.com|80|", 2),
        ("www.example.com|80|", 1),
    ]
    expects = [
        ("www.example.com|80|", 1),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_012(matcher):

    cases = [
        ("www.google.com|80|ftp", 1),
        ("www.google.com|80|http", 2),
        ("google.com|80|http", 3),
    ]
    expects = [
        ("www.google.com|80|http", 2),
        ("www.google.com|80|ftp", 1),
        ("abc.www.google.com|80|ftp", 1),
    ]

    load_and_match(matcher, cases, expects)


def test_matcher_iter_001(matcher):
    cases = [
        ("www.example.com|80|", 1),
        ("www.example.com|8080|", 2),
        (".example.com|8080|", 3),
        (".example.com||", 4),
    ]

    for netloc_string, rule in cases:
        matcher.load_from_string(netloc_string, rule)

    o = list([(str(n[0]), n[1]) for n in matcher.iter()])

    assert set(o) == set(cases)


def test_matcher_iter_002(matcher):
    cases = [
        ("www.example.com||", 1),
        ("www.example.com|80|", 2),
    ]

    for netloc_string, rule in cases:
        matcher.load_from_string(netloc_string, rule)

    o = list([(str(n[0]), n[1]) for n in matcher.iter()])

    assert set(o) == set(cases)


def test_matcher_delete_001(matcher):
    cases = [
        ("www.example.com|80|", 1),
    ]

    for netloc_string, rule in cases:
        matcher.load_from_string(netloc_string, rule)

    assert matcher.delete(Netloc("www.example.com", "", "")) == (None, None)
    assert matcher.delete(Netloc("www.example.com", "80", "")) == (
        Netloc("www.example.com", "80", ""),
        1,
    )

    o = list(matcher.iter())
    assert set(o) == set([])


def test_matcher_delete_002(matcher):
    cases = [
        ("www.example.com||", 0),
        ("www.example.com|80|", 1),
        ("www.example.com|8080|", 2),
        ("abc.example.com|8080|", 3),
    ]

    for netloc_string, rule in cases:
        matcher.load_from_string(netloc_string, rule)

    for netloc_string, rule in cases:
        netloc = Netloc.from_string(netloc_string)
        assert matcher.delete(netloc) == (netloc, rule)

    o = list(matcher.iter())
    assert set(o) == set([])


def test_matcher_delete_003(matcher):
    cases = [
        ("www.example.com||", 0),
    ]

    for netloc_string, rule in cases:
        matcher.load_from_string(netloc_string, rule)

    assert matcher.delete(Netloc.from_string("www.test.com||")) == (None, None)
    netloc = Netloc.from_string("www.example.com||")
    assert matcher.delete(netloc) == (netloc, 0)

    o = list(matcher.iter())
    assert set(o) == set([])


def test_matcher_delete_004(matcher):
    cases = [
        ("www.example.com|80|", 0),
        ("www.example.com|90|", 1),
    ]

    for netloc_string, rule in cases:
        matcher.load_from_string(netloc_string, rule)

    for netloc_string, rule in cases:
        netloc = Netloc.from_string(netloc_string)
        assert matcher.delete(netloc) == (netloc, rule)

    o = list(matcher.iter())
    assert set(o) == set([])
    assert matcher.size() == 0


def test_matcher_delete_005(matcher):
    cases = [
        ("www.example.com|80|", 0),
        ("www.example.com|90|", 1),
        ("www.example.com||", 2),
    ]

    for netloc_string, rule in cases:
        matcher.load_from_string(netloc_string, rule)

    for netloc_string, rule in cases:
        netloc = Netloc.from_string(netloc_string)
        assert matcher.delete(netloc) == (netloc, rule)

    o = list(matcher.iter())
    assert set(o) == set([])


def get_matcher_get_001(matcher):
    cases = [
        ("www.example.com|80|", 0),
        ("www.example.com|90|", 1),
        ("www.example.com||", 2),
    ]

    for netloc_string, rule in cases:
        matcher.load_from_string(netloc_string, rule)

    for netloc_string, rule in cases:
        netloc = Netloc.from_string(netloc_string)
        assert matcher.get(netloc) == (netloc, rule)

    assert matcher.get("abcd.com||") == (None, None)
