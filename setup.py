from setuptools import setup, Extension

setup(
    name = 'siteglass',
    version = '0.2',
    packages = ['siteglass'],
    ext_modules = [
        Extension('siteglass.jsmin', ['ext/jsmin.c'])
    ],
    install_requires = ['cssmin'],
    package_data = { 'siteglass': ['data/*'] },
    scripts = ['scripts/siteglass'],
    description = 'A flexible tool for merging and compressing web assets.',
    author = 'Cooper Software',
    author_email = 'elisha@cooper.com',
    url = 'https://github.com/cooper-software/siteglass',
    download_url = 'https://github.com/cooper-software/siteglass/tarball/master',
    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Pre-processors',
        'Topic :: Text Processing :: Filters'
    ]
)