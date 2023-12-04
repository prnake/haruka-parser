from setuptools import setup

# 0.1 version from OpenWebMath: https://github.com/keirp/OpenWebMath
setup(
    name="haruka_parser",
    version="0.2",
    description="Text extraction tools",
    author="",
    packages=["haruka_parser"],
    requires=["py_asciimath", "inscriptis", "tabulate", "inscriptis", "numpy"],
    include_package_data=True,
)
