from setuptools import setup, find_packages

setup(
    name="sps_crypto", 
    version="1.0.4rc",  
    author="Shourya Pratap Singh",
    author_email="sp.singh@gmail.com",
    description="Python implementation of the cryptographic algos",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/amspsingh04/sps_crypto",  # Link to your GitHub repository
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
