from ..django import env

ENABLE_TAILWIND = env.bool("ENABLE_TAILWIND")
TAILWIND_APP_NAME = "theme"
NPM_BIN_PATH_WINDOWS = env.bool("NPM_BIN_PATH_WINDOWS")

if NPM_BIN_PATH_WINDOWS:
    NPM_BIN_PATH = r"C:\Program Files\nodejs\npm.cmd"
