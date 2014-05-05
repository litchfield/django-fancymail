from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES
import os

root = os.path.dirname(os.path.abspath(__file__))
os.chdir(root)

VERSION = '0.1'

# Make data go to the right place.
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']


setup(
    name='django-fancymail',
    version=VERSION,
    description="Email templating for Django",
    long_description="Elegant templated HTML multipart emails for Django, with inline/related images and attachments",
    author="Simon Litchfield",
    author_email="simon@s29.com.au",
    url="http://github.com/litchfield/django-fancymail",
    license="MIT License",
    platforms=["any"],
    packages=['fancymail'],
    #data_files=[(template_dir, templates)],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    include_package_data=True,
)
