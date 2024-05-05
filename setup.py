from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()     

__version__ = "0.0.9"
REPO_NAME = "DiamondPricePredictionUsingMLOps"
PKG_NAME= "DiamondPricePredictionUsingMLOps"
AUTHOR_USER_NAME = "Komal-patra"
AUTHOR_EMAIL = "komalfsds2022@gmail.com"

setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A python package for connecting with database.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    packages=find_packages(),
)
