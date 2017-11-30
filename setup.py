from setuptools import setup, find_packages


kw = dict(
    name='pyct',
    version='0.0.2',
    description='python simple crontab',
    author='intohole',
    author_email='intoblack86@gmail.com',
    url='https://github.com/intohole/pyct',
    download_url='https://github.com/intohole/pyct',
    platforms='all platform',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True
)

setup(**kw)
