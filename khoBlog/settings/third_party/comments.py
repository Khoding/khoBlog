from ..django import env

COMMENTS_HIDE_REMOVED = False
COMMENTS_DISABLED_GLOBALLY = env.bool("COMMENTS_DISABLED_GLOBALLY")

COMMENTS_APP = "django_comments_xtd"
COMMENTS_XTD_CONFIRM_EMAIL = False
COMMENTS_XTD_MODEL = "comments.models.CustomCommentXTD"
COMMENTS_XTD_FORM_CLASS = "comments.forms.CustomCommentXTDForm"
COMMENTS_XTD_MAX_THREAD_LEVEL = 6

COMMENTS_XTD_APP_MODEL_OPTIONS = {
    "default": {
        "allow_flagging": True,
        "allow_feedback": True,
        "show_feedback": True,
        "who_can_post": "users",
    }
}
