import re

from ..django import BASE_DIR

with open(BASE_DIR + "/version.txt") as v_file:
    APP_VERSION_NUMBER = v_file.read()


ver = re.split(
    r"^(((v)([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?)$",
    APP_VERSION_NUMBER,
)


version = ver[3:8]


ver_code = f"{int(version[1]) * 10000 + int(version[2]) * 1000 + int(version[3]) * 100}-{version[4]}"

version_name = APP_VERSION_NUMBER
version_code = ver_code

__version__ = version_name

APP_VERSION_NAME = __version__
APP_VERSION_NUMBER = version_code

FULL_VERSION = f"{APP_VERSION_NAME} {u'–'} {APP_VERSION_NUMBER}"
