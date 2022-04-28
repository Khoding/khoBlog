from ..django import BASE_DIR

with open(BASE_DIR + "/version.txt") as v_file:
    APP_VERSION_NUMBER = v_file.read()

major = APP_VERSION_NUMBER.split(".")[0]
minor = APP_VERSION_NUMBER.split(".")[1]
patch, build = APP_VERSION_NUMBER.split(".")[2].split("-")

ver_code = f"{int(major) * 10000 + int(minor) * 1000 + int(patch) * 100}-{build}"

version_code = ver_code
version_name = f"v{major}.{minor}.{patch}-{build}"

__version__ = version_name

APP_VERSION_NAME = __version__
APP_VERSION_NUMBER = version_code

FULL_VERSION = f"{APP_VERSION_NAME} {u'–'} {APP_VERSION_NUMBER}"
