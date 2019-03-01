import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rxe",
    version="0.9",
    author="Marton Trencseni",
    author_email="mtrencseni@gmail.com",
    description="Literate and composable regular expressions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mtrencseni/rxe",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: Unlicense",
        "Operating System :: OS Independent",
    ],
)