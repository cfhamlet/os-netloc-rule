from os_netloc_rule.utils import split_netloc


def test_split_domain_port():

    cases = [
        (("www.baidu.com", None), ("www.baidu.com", None)),
        (("www.baidu.com:88", None), ("www.baidu.com", "88")),
        (("www.baidu.com", "http"), ("www.baidu.com", "80")),
        (("www.baidu.com:99", "http"), ("www.baidu.com", "99")),
        (("127.0.0.1", "ssh"), ("127.0.0.1", "22")),
    ]

    for netloc_and_schema, expected in cases:
        assert expected == split_netloc(*netloc_and_schema)
