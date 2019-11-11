import os_netloc_rule


def test_version():
    import os

    this_file = os.path.abspath(__file__)
    v = this_file.split(os.pathsep)[:-2] + ["src", "os_netloc_rule", "VERSION"]
    version_file = os.path.join(*v)
    assert os_netloc_rule.__version__ == open(str(version_file)).read().strip()


if __name__ == "__main__":
    test_version()
