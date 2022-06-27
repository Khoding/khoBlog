from ..django import BASE_DIR

PWA_SERVICE_WORKER_PATH = BASE_DIR + "static/js/" + "serviceworker.js"

PWA_APP_NAME = "Khodok's Blog"
PWA_APP_DESCRIPTION = "Khodok's Blog"
PWA_APP_THEME_COLOR = "#B362FF"
PWA_APP_BACKGROUND_COLOR = "#B362FF"
PWA_APP_DISPLAY = "standalone"
PWA_APP_SCOPE = "/"
PWA_APP_ORIENTATION = "any"
PWA_APP_START_URL = "/"
PWA_APP_STATUS_BAR_COLOR = "default"
PWA_APP_ICONS = [
    {
        "src": "static/khoBlog/img/RuthinkkTooBig-small.png",
    }
]
PWA_APP_ICONS_APPLE = [
    {
        "src": "static/khoBlog/img/RuthinkkTooBig-small.png",
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        "src": "static/khoBlog/img/RuthinkkTooBig.webp",
        "media": "(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)",
    }
]
PWA_APP_DIR = "ltr"
PWA_APP_LANG = "en-GB"
