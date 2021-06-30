major = 0
minor = 9
patch = 7
build = 0

version_code = major * 10000 + minor * 1000 + patch * 100 + build
version_name = f"{major}.{minor}.{patch}"

__version__ = version_name

APP_VERSION_NAME = __version__
APP_VERSION_NUMBER = version_code
