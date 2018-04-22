from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='km2events',
    version='0.1',
    keywords='knowledge-model transformation dsw events json',
    description='Simple tool to transform Knowledge Model to Events',
    long_description=long_description,
    author='Marek Suchánek',
    author_email='marek.suchanek@fit.cvut.cz',
    license='MIT',
    url='https://github.com/DataStewardshipWizard/km2events',
    zip_safe=False,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dsw-km2events = km2events:cli',
        ]
    },
    install_requires=[
        'click'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)