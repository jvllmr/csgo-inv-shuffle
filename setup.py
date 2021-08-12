import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csgoinvshuffle",
    version="1.0.3b1",
    author="Jan Vollmer",
    author_email="zunder325@gmail.com",
    description="A Python package for creating CS:GO shuffle config files. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kreyoo/csgo-inv-shuffle",
    project_urls={
        "Bug Tracker": "https://github.com/kreyoo/csgo-inv-shuffle/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'requests',
      ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9",
)
