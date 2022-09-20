from setuptools import setup

setup(name='yanecis',
      version='0.1',
      description='Yet Another Electrical Circuit Solver',
      author='Heritier Kinke',
      author_email='heritier.kinke@yandex.com',
      url='https://github.com/hkinke/yanecis',
      packages=['yanecis'],
      package_dir={'':'src'},
      install_requires=['numpy']
     )