from setuptools import find_packages, setup


def read(*filenames, **kwargs):
    import io
    from os.path import join, dirname

    encoding = kwargs.get("encoding", "utf-8")
    sep = kwargs.get("sep", "\n")
    buf = []
    for filename in filenames:
        with io.open(join(dirname(__file__), filename), encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


setup(
    name="os-netloc-rule",
    version=read("src/os_netloc_rule/VERSION").strip(),
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    license="MIT License",
    description="A common library for netloc rule use case.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Ozzy",
    author_email="cfhamlet@gmail.com",
    url="https://github.com/cfhamlet/os-netloc-rule",
    install_requires=open("requirements/requirements.txt").read().split("\n"),
    python_requires=">=2.7",
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
