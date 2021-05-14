from django.db import models
import auto_prefetch


class PostQuerySet(auto_prefetch.QuerySet):
    def get_by_author(self, author_username):
        return self.filter(author__username=author_username)

    def get_by_tags(self, tags_name):
        return self.filter(tags__name=tags_name)

    def get_by_clicks(self):
        return self.order_by('clicks')


class PostManager(auto_prefetch.Manager):

    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def get_by_author(self, author_username):
        return self.get_queryset().get_by_author(author_username)

    def get_by_tags(self, tags_name):
        return self.get_queryset().get_by_tags(tags_name)

    def get_by_clicks(self):
        return self.get_queryset().get_by_clicks()
