import auto_prefetch
from django.db.models.query_utils import Q
from django.utils import timezone


class PostQuerySet(auto_prefetch.QuerySet):
    def get_without_removed(self):
        return self.filter(is_removed=False)

    def get_base_common_queryset(self):
        return self.filter(Q(published_date__lte=timezone.now(), withdrawn=False, is_removed=False))

    def get_common_queryset(self, user):
        if user.is_superuser:
            return self.filter(is_removed=False)
        else:
            return self.filter(Q(published_date__lte=timezone.now(), withdrawn=False, is_removed=False))

    def get_by_author(self, author_username):
        return self.filter(author__username=author_username)

    def get_by_tags(self, tags_name):
        return self.filter(tags__name=tags_name)

    def get_by_clicks(self):
        return self.order_by('clicks')


class PostManager(auto_prefetch.Manager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def get_without_removed(self):
        return self.get_queryset().get_without_removed()

    def get_base_common_queryset(self):
        return self.get_queryset().get_base_common_queryset()

    def get_common_queryset(self, user):
        return self.get_queryset().get_common_queryset(user)

    def get_by_author(self, author_username):
        return self.get_queryset().get_by_author(author_username)

    def get_by_tags(self, tags_name):
        return self.get_queryset().get_by_tags(tags_name)

    def get_by_clicks(self):
        return self.get_queryset().get_by_clicks()


class CategoryQuerySet(auto_prefetch.QuerySet):
    def get_without_removed(self):
        return self.filter(is_removed=False)


class CategoryManager(auto_prefetch.Manager):

    def get_queryset(self):
        return SeriesQuerySet(self.model, using=self._db)

    def get_without_removed(self):
        return self.get_queryset().get_without_removed()


class SeriesQuerySet(auto_prefetch.QuerySet):
    def get_without_removed(self):
        return self.filter(is_removed=False)


class SeriesManager(auto_prefetch.Manager):

    def get_queryset(self):
        return SeriesQuerySet(self.model, using=self._db)

    def get_without_removed(self):
        return self.get_queryset().get_without_removed()
