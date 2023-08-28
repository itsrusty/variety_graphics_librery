import pathlib
from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent

VERSION = '0.0.1'
PACKAGE_NAME = 'easy_graphic' 
AUTHOR = 'Hiram Gabriel'
AUTHOR_EMAIL = 'rusty3031@gmail.com'
URL = 'https://github.com/itsrusty' 

LICENSE = 'MIT' #Tipo de licencia
DESCRIPTION = 'Librería para crear diferentes figuras y un FPS con ursina' #Descripción corta
LONG_DESCRIPTION = (HERE / "README.md").read_text(encoding='utf-8') #Referencia al documento README con una descripción más elaborada
LONG_DESC_TYPE = "text/markdown"

INSTALL_REQUIRES = [
      'ursina',
      "turtle"
      ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESC_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True
)
