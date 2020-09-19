import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="httpython",
    version="0.2.6",
    author="Jão Bernardi",
    author_email="joao_bernardi@outlook.com",
    description="A simple-to-use framework for http and https servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaobernardi/Httpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)