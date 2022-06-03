import re

from setuptools import setup


with open("ccli/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)


setup(
    name="ccli",
    version=version,
    author="reecehughes",
    url="https://github.com/ReeceHughes/CCLI",
    description="Chain Command Line Interface",
    long_description=open("README.md").read(),
    packages=["ccli"],
    python_requires=">=3",
)

