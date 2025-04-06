from setuptools import setup, find_packages

setup(
    name="sps_crypto",
    version="1.0.6a",  # Follow PEP 440 versioning
    author="Shourya Pratap Singh",
    author_email="sp.singh@gmail.com",
    description="Python implementation of cryptographic algorithms including RSA, ElGamal, AES, and more",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amspsingh04/sps_crypto",
    packages=find_packages(where=".", exclude=["tests*", "examples*"]),
    package_dir={"": "."},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",
    keywords="cryptography rsa elgamal aes des diffie-hellman",
    project_urls={
        "Bug Reports": "https://github.com/amspsingh04/sps_crypto/issues",
        "Source": "https://github.com/amspsingh04/sps_crypto",
    },
)