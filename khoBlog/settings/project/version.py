from ..django import BASE_DIR

with open(BASE_DIR + "/version.txt") as v_file:
    APP_VERSION_NUMBER = v_file.read()

major = int(APP_VERSION_NUMBER.split('.')[0])
minor = int(APP_VERSION_NUMBER.split('.')[1])
patch = int(APP_VERSION_NUMBER.split('.')[2])
build = APP_VERSION_NUMBER.split('.')[3]

if isinstance(build, str):
    ver_code = f"{major * 10000 + minor * 1000 + patch * 100}{build}"
else:
    ver_code = f"{major * 10000 + minor * 1000 + patch * 100 + build}"

version_code = ver_code
version_name = f"{major}.{minor}.{patch}-{build}"

__version__ = version_name

APP_VERSION_NAME = __version__
APP_VERSION_NUMBER = version_code
