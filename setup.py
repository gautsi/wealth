
import setuptools


with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="wealth_ineq_sim",
    version="0.0.1",
    author="Gautam Sisodia",
    packages=setuptools.find_packages(),
    classifiers=["Progamming Language :: Python :: 3"],
)