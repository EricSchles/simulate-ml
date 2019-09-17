import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="simulate_ml",
    version="0.01",
    description="an active learning and simulation framework",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/EricSchles/simulate-ml",
    author="Eric Schles",
    author_email="ericschles@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["simulate_ml", 'simulate_ml.active_learning'],
    include_package_data=True,
    install_requires=["sklearn", "scipy", "numpy", "statsmodels", "mlxtend", "pytest"],
)
