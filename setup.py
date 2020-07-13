from setuptools import setup

setup(name='dominion-object-model',
      version='1.0.0',
      url='https://github.com/the-gigi/dominion/dominion/object_model',
      license='MIT',
      author='Gigi Sayfan',
      author_email='the.gigi@gmail.com',
      description='abstract classes for implementing dominion-object-model players and clients',
      packages=['dominion.object_model'],
      package_data={'dominion.object_model': ['README.md', 'LICENSE']},
      python_requires='>=3.8',
      long_description=open('dominion/object_model/README.md').read(),
      long_description_content_type="text/markdown",
      zip_safe=False)
