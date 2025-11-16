from setuptools import setup, find_packages

setup(
    name="revoregex",
    version="0.1.0",
    description="A multilingual regex library for Python (Turkish, English, German, French, and more)",
    author="Barış Aksel",
    author_email="iletisim@barisaksel.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Turkish",
        "Natural Language :: English",
        "Natural Language :: German",
        "Natural Language :: French",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta"
    ],
    keywords="regex validation multilingual i18n internationalization Turkish English German French IBAN credit-card phone email domain python luhn mod97 json html uuid mac plate password username open-source PyPI form-validation data-validation",
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Source": "https://github.com/Barisaksel/RevoRegex",
        "Bug Tracker": "https://github.com/Barisaksel/RevoRegex/issues"
    },
)