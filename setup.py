from setuptools import setup, find_packages

# Package name
name = 'unrealspeech'

# Version number
version = '0.1.1'

# Package description
description = 'A Python package for interacting with the Unreal Speech API.'

# Author information
author = 'Ajaga Abdulbasit'
author_email = 'basitng2004@gmail.com'

# URL for the package's homepage or repository
url = 'https://github.com/basitng/unrealspeech'

# License information
license = 'MIT'

install_requires = [
    'requests',
    'soundfile',
    'sounddevice'
]

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    packages=find_packages(),
    author_email=author_email,
    url=url,
    license=license,
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=install_requires,
)
