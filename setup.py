from setuptools import setup

# 0.1 version from OpenWebMath: https://github.com/keirp/OpenWebMath
# OpenWebMath is made available under an ODC-By 1.0 license; users should also abide by the CommonCrawl ToU: https://commoncrawl.org/terms-of-use/. We do not alter the license of any of the underlying data.
setup(
    name="haruka_parser",
    version="0.2.0",
    description="A simple HTML Parser",
    author="papersnake",
    author_email="prnake@gmail.com",
    url="https://github.com/prnake/haruka-parser",
    packages=["haruka_parser"],
    install_requires=["py_asciimath", "inscriptis", "tabulate", "numpy", "resiliparse"],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Utilities",
    ),
)
