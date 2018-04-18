from setuptools import setup, find_packages

setup(name='yiiepapi-py',
    version='0.1',
    url='https://github.com/numerums/yiiepapi-py',
    license='MIT',
    author='Numerum Services',
    author_email='numerums@outlook.com',
    description='Python API for Yiiep payment platform',
    keywords='yiiep payment mobile money api cfa',
    packages='yiiepapi',
    long_description=open('README.md').read(),
    zip_safe=False,
    install_requires=['requests'])