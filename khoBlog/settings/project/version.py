major = 0
minor = 4
patch = 2

version_code = major * 1000 + minor * 100 + patch * 10
version_name = f"{major}.{minor}.{patch}"

__version__ = version_name

APP_VERSION_NAME = __version__
APP_VERSION_NUMBER = version_code
