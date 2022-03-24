from setuptools import find_packages, setup
from os import path

with open('requirements.txt') as f:
    requirements = [req for req in f if req.strip()]
   
# Get the long description from the README file
here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md")) as f:
    readme = f.read()
     
setup(
    name="easy_web",
    version=1.0,
    description="easy_web helps you easily build web applications",
    license="MIT License",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="",
    python_requires=">=3.8, <3.9",
    packages=find_packages(exclude=["docs*", "tests*"]),
    include_package_data=True,
    author="Amir",
    entry_points={"console_scripts": ["easy_web = easy_web:main"]},
    keywords="web development, python",
    install_requires=requirements,
)