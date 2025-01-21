from setuptools import setup, find_packages

setup(
    name="oneMillion",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "websockets",
        "requests",
        "pytest",
        "pytest-asyncio"
    ],
    python_requires=">=3.8",
) 