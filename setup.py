from os import path

from setuptools import setup

with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
    readme_description = f.read()


def read_requirements(filename):
    with open(filename, "r", encoding="utf-8") as fp:
        return fp.read().strip().splitlines()


setup(
    name="miko",
    packages=["miko"],
    version="1.0",
    license="MIT License",
    description="See how to use a Python object at a glance!",
    author="Anime no Sekai",
    author_email="niichannomail@gmail.com",
    url="https://github.com/Animenosekai/miko",
    download_url="https://github.com/Animenosekai/miko/archive/v1.0.tar.gz",
    keywords=[
        "python",
        "documentation",
        "miko",
        "docs"
    ],
    install_requires=read_requirements("requirements.txt"),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    long_description=readme_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    python_requires=">=3.4, <4",
    entry_points={"console_scripts": ["miko = miko.__main__:main"]},
    package_data={
        "miko": ["LICENSE"],
    },
)
