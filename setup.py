from setuptools import setup, find_packages


setup(
    name='CveParser',
    version='0.1',
    packages=find_packages(),

    install_requires=[
        'beautifulsoup4 < 4.4',
        'argparse < 1.3',
    ],

    entry_points={
        'console_scripts': [
            'cve = src.cve:main',
        ],

    },
)
