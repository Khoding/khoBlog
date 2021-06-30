from ..django import BASE_DIR

with open(BASE_DIR + "/version.txt") as v_file:
    APP_VERSION_NUMBER = v_file.read()

major = int(APP_VERSION_NUMBER.split('.')[0])
minor = int(APP_VERSION_NUMBER.split('.')[1])
patch = int(APP_VERSION_NUMBER.split('.')[2])

version_code = major * 1000 + minor * 100 + patch * 10
version_name = f"{major}.{minor}.{patch}"

__version__ = version_name

APP_VERSION_NAME = __version__
APP_VERSION_NUMBER = version_code
