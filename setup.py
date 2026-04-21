from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip()]

setup(
    name="Hammer",
    version="1.0.0",
    author="Kanax01",
    description="A network stress testing tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kanax01/Hammer",
    py_modules=["hammer", "referers", "useragents"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hammer=hammer:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
