def get_model():
    """Get model"""
    from comments.models import CustomComment

    return CustomComment


def get_form():
    """Get form"""
    from comments.forms import CustomCommentForm

    return CustomCommentForm
