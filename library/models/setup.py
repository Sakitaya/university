import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="models",
    version="0.1.0",
    author="Akitaya Shunichi",
    author_email="c0118004c5@edu.teu.ac.jp",
    description="This library is used to monitor the state of the doktor microservice, a thesis search service.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akitaya0519/micro-service",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={},
    python_requires='>=3.8',
)