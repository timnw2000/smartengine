from setuptools import setup

with open("requirements.txt", "r") as r:
    install_requires = r.readlines()

with open("README.md", "r") as long_description:
    long_description = long_description.read()

    
setup(
    name="smartengine",
    version="0.1.0",
    description="A small library that simplifies the use of the smartengine rAPI",
    long_description=long_description,
    long_description_content_type="text/markdown"
    author="Tim Nwungang",
    author_email="timnw.dev@gmail.com",
    url="https://github.com/timnw2000/smartengine",
    requires=["setuptools"],
    install_requires=install_requires,
)