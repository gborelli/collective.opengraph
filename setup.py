from setuptools import setup, find_packages
import os

version = '1.0'
tests_require = ['plone.app.testing']

setup(name='collective.opengraph',
      version=version,
      description="Plone opengraph",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Giorgio Borelli',
      author_email='giorgio@giorgioborelli.it',
      url='http://plone.org/products/collective.opengraph',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'ordereddict',
          # -*- Extra requirements: -*-
      ],
      extras_require=dict(test=tests_require),
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
