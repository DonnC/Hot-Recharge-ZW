import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hot-recharge",
    version="3.3.1",
    author="Donald Chinhuru",
    author_email="donychinhuru@gmail.com",
    description="perform hot-recharge services with hot-recharge library programmatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonnC/Hot-Recharge-ZW",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=["munch"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
