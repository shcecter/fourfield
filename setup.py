import pathlib
from setuptools import setup, find_packages


README = (pathlib.Path(__file__).parent / "README.md").read_text()  # the text of readme file

setup(
    name="fourfield",
    version="0.0.1",
    description="Script for generating four field weighing reports",
    long_description=README,
    long_description_content_type="text/markdown",
    author="shcecter",
    author_email="shcecter@mail.ru",
    packages=find_packages(),
    install_requires=["pandas", "numpy", "matplotlib", "fpdf", "click"],
    )