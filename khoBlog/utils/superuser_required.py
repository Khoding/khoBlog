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
        class WrappedClass(UserPassesTestMixin, wrapped):
            """WrappedClass"""

            def test_func(self):
                return self.request.user.is_superuser

        return WrappedClass

    return wrapper
