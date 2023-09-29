import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hapi_schema",
    version="0.0.5",
    author="HDX",
    author_email="simon.johnson@un.org",
    description="HAPI database schema specified in SQLAlchemy",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/OCHA-DAP/hapi-sqlalchemy-schema",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'sqlalchemy',
        'hdx-python-api'
    ]
)