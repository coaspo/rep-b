import setuptools
import ltrans
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ltrans",
    version="0.0.1",
    author="C Hantzis",
    author_email="author@example.com",
    description="A small example package",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/translator",
    packages=setuptools.find_packages(exclude=['tests']),
    test_suite="tests",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

# to setup may add:
# entry_points={'console_scripts': ['run = mypkg.module::run'
# to add functions as command line tools, for example to start web server

#install_requires=['numpy=1.8.1',   ,,],
