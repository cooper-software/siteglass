from setuptools import setup

setup(
    name = 'siteglass',
    version = '0.1',
    packages = ['siteglass'],
    package_data = { 'siteglass': ['data/*'] },
    scripts = ['scripts/siteglass'],
    requires = ['jsmin', 'cssmin'],
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