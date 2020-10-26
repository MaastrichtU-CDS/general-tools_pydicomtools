import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydicomtools", # Replace with your own username
    version="0.0.1",
    author="Johan van Soest",
    author_email="johan.vansoest@maastro.nl",
    description="A small example package with DICOM tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/UM-CDS/general-tools/pydicomtools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pydicom'
    ]
)