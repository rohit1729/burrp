from setuptools import setup, find_packages

setup(
    name="burrp",
    version="0.1.0",
    description="Organize your files with local AI",
    author="Burrp Team",
    packages=find_packages(),
    install_requires=[
        "ollama>=0.1.0",
    ],
    entry_points={
        "console_scripts": [
            "burrp=burrp:main",
        ],
    },
    python_requires=">=3.7",
)
