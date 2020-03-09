import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# TODO Implement api requests using `requests` module
REQUIRED = [
    'requests'
]

setuptools.setup(
    name="hot-recharge",
    version="1.2.0",
    author="Donald Chinhuru",
    author_email="donychinhuru@gmail.com",
    description="perform hot recharge transactions via web service library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DonnC/Hot-Recharge-ZW",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
)
