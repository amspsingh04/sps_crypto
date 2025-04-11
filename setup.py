from setuptools import setup, find_packages
import pathlib

# Read the long description from README.md
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="sps_crypto",
    version="1.0.79",  # Follow PEP 440 versioning
    author="Shourya Pratap Singh",
    author_email="sp.singh@gmail.com",
    description="Pure-Python implementation of cryptographic algorithms (RSA, ElGamal, AES, DES, Diffie-Hellman)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amspsingh04/sps_crypto",
    project_urls={
        "Bug Reports": "https://github.com/amspsingh04/sps_crypto/issues",
        "Source": "https://github.com/amspsingh04/sps_crypto",
        "Documentation": "https://github.com/amspsingh04/sps_crypto/blob/main/README.md",
    },

    python_requires=">=3.7",
    install_requires=[
        'cryptography>=3.4',  # For secure random number generation
    ],
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.0',
            'mypy>=0.910',
            'flake8>=3.9',
        ],
        'docs': [
            'sphinx>=4.0',
            'sphinx-rtd-theme>=0.5',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    keywords=[
        "cryptography", 
        "educational",
        "rsa", 
        "elgamal", 
        "aes", 
        "des", 
        "diffie-hellman",
        "digital signatures",
    ],
    package_data={
        "sps_crypto": ["py.typed"],
    },
    entry_points={
        'console_scripts': [
            'sps-crypto-demo=sps_crypto.cli:demo',
        ],
    },
    zip_safe=False,
)