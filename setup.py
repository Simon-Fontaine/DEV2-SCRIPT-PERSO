from setuptools import setup, find_packages

setup(
    name="inventory_manager",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas>=1.3.0",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Système de gestion d'inventaire",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
)
