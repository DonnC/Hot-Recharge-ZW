import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIRED = [
    'requests'
]

setuptools.setup(
    name="hot-recharge",
    version="1.1.0",
    author="Donald Chinhuru",
    author_email="donychinhuru@gmail.com",
    description="perform hot recharge transactions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonnC/Hot-Recharge-ZW",
    license="MIT",
    install_requires=REQUIRED,
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
