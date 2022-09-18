from django.contrib.auth.mixins import UserPassesTestMixin


def superuser_required():
    """superuser_required Decorator

    A utility to test if a user is a superuser before giving access to a view
    from khoBlog.utils.superuser_required import superuser_required

    @superuser_required
    class ExampleView(View):
        ...
    """

    def wrapper(wrapped):
        """Wrapper"""

        class WrappedClass(UserPassesTestMixin, wrapped):
            """WrappedClass"""

            def test_func(self):
                """test_func"""
                return self.request.user.is_superuser and self.request.user.secure_mode is False

        return WrappedClass

    return wrapper


def superuser_required_ignore_secure_mode():
    """superuser_required_ignore_secure_mode Decorator

    A utility to test if a user is a superuser before giving access to a view
    from khoBlog.utils.superuser_required import superuser_required_ignore_secure_mode

    @superuser_required_ignore_secure_mode
    class ExampleView(View):
        ...
    """

    def wrapper(wrapped):
        """Wrapper"""

        class WrappedClass(UserPassesTestMixin, wrapped):
            """WrappedClass"""

            def test_func(self):
                """test_func"""
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper
