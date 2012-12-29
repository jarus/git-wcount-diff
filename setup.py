from setuptools import setup

setup(
    name='git-wcount-diff',
    version='0.1',
    url='http://github.com/jarus/git-wcount-diff/',
    license='BSD',
    author='Christoph Heer',
    author_email='Christoph.Heer@googlemail.com',
    description='Script to analyse the diff of removed/added words and ' \
                'characters between git revisions',
    py_modules=['git_wcount_diff'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['git-wcount-diff = git_wcount_diff:main'],
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
