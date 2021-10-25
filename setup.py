from setuptools import setup, find_packages
from status_notifier import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()


install_requires = []


setup(
    name="status-notifier-app",
    version=__version__,
    author="Pedro Jorge Nunes",
    author_email="pjn2work@google.com",
    description="Python app to notify, via slack channel you choose to be notified, for the status_code change from the URL list you setup to be checked every yy seconds",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pjn2work/status_notifier",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires
)
