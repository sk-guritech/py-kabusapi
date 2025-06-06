from setuptools import find_packages, setup

setup(
    name="py-kabusapi",
    version="1.0.0",
    description="Python wrapper for kabuステーション API",
    author="Sakaguchi Ryo",
    author_email="sakaguchi@sk-techfirm.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pydantic",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
