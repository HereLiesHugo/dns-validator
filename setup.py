from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="dns-validator",
    version="1.0.0",
    author="DNS Validator Team",
    author_email="contact@dnsvalidator.com",
    description="A comprehensive DNS validation tool with delegation, propagation, and provider settings checks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HereLiesHugo/dns-validator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Topic :: Internet :: Name Service (DNS)",
        "Topic :: System :: Networking",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "dns-validator=dns_validator:cli",
            "dnsval=dns_validator:cli",
        ],
    },
    keywords="dns validation delegation propagation cloudflare nameservers cli",
    project_urls={
        "Bug Reports": "https://github.com/HereLiesHugo/dns-validator/issues",
        "Source": "https://github.com/HereLiesHugo/dns-validator",
        "Documentation": "https://github.com/HereLiesHugo/dns-validator#readme",
    },
)