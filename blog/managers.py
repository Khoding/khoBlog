import auto_prefetch
from django.utils import timezone


class PostQuerySet(auto_prefetch.QuerySet):
    """PostQuerySet

    A custom QuerySet for Post

    Args:
        auto_prefetch ([type]): [description]
    """

    def get_without_removed(self):
        """Get without removed"""
        return self.filter(deleted_at=None)

    def get_base_common_queryset(self):
        """Get base common queryset"""
        return self.defer("body", "image").filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None)

    def get_common_queryset(self, user):
        """Get common queryset"""
        if user.is_superuser and user.secure_mode is False:
            queryset = self.defer("body", "image").filter(deleted_at=None)
        else:
            queryset = self.defer("body", "image").filter(
                pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None
            )
        return queryset

    def get_without_wednesday(self):
        """Get without wednesday"""
        return self.exclude(categories__slug__iexact="wednesday")

    def get_by_author(self, author_username):
        """Get by author"""
        return self.filter(author__username=author_username)

    def get_by_tags(self, tags_name):
        """Get by tags"""
        return self.filter(tags__name=tags_name)

    def get_by_clicks(self):
        """Get by clicks"""
        return self.order_by("-clicks")


class PostManager(auto_prefetch.Manager):
    """PostManager

    A custom Manager for Post

    Args:
        auto_prefetch ([type]): [description]
    """

    def get_queryset(self):
        """Get queryset"""
        return PostQuerySet(self.model, using=self._db)

    def get_without_removed(self):
        """Get without removed"""
        return self.get_queryset().get_without_removed()

    def get_without_wednesday(self):
        """Get without wednesday"""
        return self.get_queryset().get_without_wednesday()

    def get_base_common_queryset(self):
        """Get base common queryset"""
        return self.get_queryset().get_base_common_queryset()

    def get_common_queryset(self, user):
        """Get common queryset"""
        return self.get_queryset().get_common_queryset(user)

    def get_by_author(self, author_username):
        """Get by author"""
        return self.get_queryset().get_by_author(author_username)

    def get_by_tags(self, tags_name):
        """Get by tags"""
        return self.get_queryset().get_by_tags(tags_name)

    def get_by_clicks(self):
        """Get by clicks"""
        return self.get_queryset().get_by_clicks()


class CategoryQuerySet(auto_prefetch.QuerySet):
    """CategoryQuerySet

    A custom QuerySet for Category

    Args:
        auto_prefetch ([type]): [description]
    """

    def get_without_removed(self):
        """Get without removed"""
        return self.filter(deleted_at=None)

    def get_base_common_queryset(self):
        """Get base common queryset"""
        return self.filter(withdrawn=False, deleted_at=None)

    def get_common_queryset(self, user):
        """Get common queryset"""
        if user.is_superuser and user.secure_mode is False:
            queryset = self.filter(deleted_at=None)
        else:
            queryset = self.filter(withdrawn=False, deleted_at=None)
        return queryset


class CategoryManager(auto_prefetch.Manager):
    """CategoryManager

    A custom Manager for Category

    Args:
        auto_prefetch ([type]): [description]
    """

    def get_queryset(self):
        """Get queryset"""
        return CategoryQuerySet(self.model, using=self._db)

    def get_without_removed(self):
        """Get without removed"""
        return self.get_queryset().get_without_removed()

    def get_base_common_queryset(self):
        """Get base common queryset"""
        return self.get_queryset().get_base_common_queryset()

    def get_common_queryset(self, user):
        """Get common queryset"""
        return self.get_queryset().get_common_queryset(user)


class SeriesQuerySet(auto_prefetch.QuerySet):
    """SeriesQuerySet

    A custom QuerySet for Series

    Args:
        auto_prefetch ([type]): [description]
    """

    def get_without_removed(self):
        """Get without removed"""
        return self.filter(deleted_at=None)

    def get_base_common_queryset(self):
        """Get base common queryset"""
        return self.filter(withdrawn=False, deleted_at=None)


class SeriesManager(auto_prefetch.Manager):
    """SeriesManager

    A custom Manager for Series

    Args:
        auto_prefetch ([type]): [description]
    """

    def get_queryset(self):
        """Get queryset"""
        return SeriesQuerySet(self.model, using=self._db)

    def get_without_removed(self):
        """Get without removed"""
        return self.get_queryset().get_without_removed()

    def get_base_common_queryset(self):
        """Get base common queryset"""
        return self.get_queryset().get_base_common_queryset()
