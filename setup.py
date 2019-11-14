from setuptools import setup, find_packages

setup(
        name='recipes',
        version='0.1',
        description='cooking recipes ...',
        author='Baiyue Cao',
        author_email='caobaiyue@gmail.com',
        license='MIT',
        pacakges=find_packages(),
        install_requires=[
            'click',
            'psycopg2-binary',
            'sqlalchemy',
            'xlrd',
            'requests'],
        entry_points='''
        [console_scripts]
        cook=recipes.cli:cli
      '''
    )