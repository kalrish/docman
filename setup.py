import setuptools


packages = setuptools.find_packages(
)

setuptools.setup(
    entry_points={
        'console_scripts': [
            'docman = docman.cli.main:entry_point',
        ],
    },
    install_requires=[
        'boto3 == 1.12.19',
        'pyxdg == 0.26',
        'PyYAML == 5.4',
    ],
    name='docman',
    package_data={
        'docman': [
            'data/*',
        ],
    },
    packages=packages,
    # f-strings were introduced in 3.6
    # Required argument was added to argparse.add_subparsers in 3.7
    # importlib.resources was added in 3.7
    python_requires='>= 3.7',
    version='1.0',
)
