import datetime
import itertools

import auto_prefetch
import rules
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from rules.contrib.models import RulesModelBase, RulesModelMixin
from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager

from blog.managers import CategoryManager, PostManager, SeriesManager
from custom_taggit.models import CustomTaggedItem


class Category(RulesModelMixin, auto_prefetch.Model, metaclass=RulesModelBase):
    parent = auto_prefetch.ForeignKey(
        'self', on_delete=models.CASCADE, related_name="category_children", null=True, blank=True)
    title = models.CharField(max_length=200, help_text="Category title")
    description = models.TextField(
        blank=True, help_text="Category description")
    slug = models.SlugField(unique=True, default="",
                            max_length=200, help_text="Category slug")
    withdrawn = models.BooleanField(
        default=False, help_text="Is Category withdrawn")
    is_removed = models.BooleanField('is removed', default=False, db_index=True,
                                     help_text=('Soft delete'))
    history = HistoricalRecords()

    objects = CategoryManager()

    class Meta:
        ordering = ['pk']
        verbose_name_plural = "Categories"
        rules_permissions = {
            "add": rules.is_superuser,
            "update": rules.is_superuser,
        }

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_category_list', kwargs={'slug': self.slug})

    def get_absolute_update_url(self):
        return reverse('blog:category_edit', kwargs={'slug': self.slug})

    def get_absolute_delete_url(self):
        return reverse('blog:category_remove', kwargs={'slug': self.slug})

    def get_absolute_admin_update_url(self):
        return reverse('admin:blog_category_change', kwargs={'object_id': self.pk})

    def remove(self):
        self.is_removed = True
        self.save()

    @property
    def get_post_count_in_category(self):
        return self.postcatslink_set.filter(post__published_date__lte=timezone.now(), post__withdrawn=False,
                                            post__is_removed=False).count()

    @property
    def get_superuser_post_count_in_category(self):
        return self.postcatslink_set.filter(post__is_removed=False).count()

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(
            self.__class__)
        return reverse("%s:%s_list" % (content_type.app_label, content_type.model))


class Series(RulesModelMixin, auto_prefetch.Model, metaclass=RulesModelBase):
    title = models.CharField(max_length=200, help_text="Series title")
    description = models.TextField(blank=True, help_text="Series description")
    slug = models.SlugField(unique=True, default="",
                            max_length=200, help_text="Series slug")
    withdrawn = models.BooleanField(
        default=False, help_text="Is Series withdrawn")
    is_removed = models.BooleanField('is removed', default=False, db_index=True,
                                     help_text=('Soft delete'))
    history = HistoricalRecords()

    objects = SeriesManager()

    class Meta:
        rules_permissions = {
            "add": rules.is_superuser,
            "update": rules.is_superuser,
        }
        ordering = ['pk']
        verbose_name_plural = "Series"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_series_list', kwargs={'slug': self.slug})

    def get_absolute_update_url(self):
        return reverse('blog:series_edit', kwargs={'slug': self.slug})

    def get_absolute_delete_url(self):
        return reverse('blog:series_remove', kwargs={'slug': self.slug})

    def get_absolute_admin_update_url(self):
        return reverse('admin:blog_series_change', kwargs={'object_id': self.pk})

    def remove(self):
        self.is_removed = True
        self.save()

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(
            self.__class__)
        return reverse("%s:%s_list" % (content_type.app_label, content_type.model))


class PostCatsLink(auto_prefetch.Model):
    post = auto_prefetch.ForeignKey(
        'blog.Post', on_delete=models.CASCADE)
    category = auto_prefetch.ForeignKey(
        'blog.Category', on_delete=models.CASCADE)
    featured_cat = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Post to Category Link"

    def __str__(self):
        return '%s - %s' % (self.post.title, self.category.title)


class Post(RulesModelMixin, auto_prefetch.Model, metaclass=RulesModelBase):
    PUBLICATION_CHOICES = [
        ('P', 'Published'),
        ('W', 'Withdrawn'),
        ('D', 'Draft'),
    ]

    FEATURING_CHOICES = [
        ('F', 'Featured'),
        ('FB', 'Featured Big'),
        ('N', 'Not Featured'),
    ]

    LANGUAGE_CHOICES = [
        ('EN', 'English'),
        ('FR', 'French'),
        ('ML', 'Multi Linguistic'),
        ('OL', 'Other Language'),
        ('NS', 'Not Specified'),
    ]

    author = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_author", help_text="Post author")
    title = models.CharField(max_length=200, help_text="Post title")
    featured_title = models.CharField(
        max_length=27, default='', blank=True, help_text="Featured post title")
    body = MarkdownxField(help_text="Post main content", blank=True)
    image = models.ImageField(
        null=True, blank=True, upload_to='images/post/', help_text="Post image")
    description = models.TextField(help_text="Post description")
    slug = models.SlugField(unique=True, max_length=200, help_text="Post slug")
    categories = models.ManyToManyField(
        'blog.Category', through='PostCatsLink', help_text="Post categories")
    tags = TaggableManager(blank=True, through=CustomTaggedItem)
    series = auto_prefetch.ForeignKey(
        'blog.Series', on_delete=models.CASCADE, related_name="post_series", help_text="Post series", blank=True,
        null=True)
    order_in_series = models.PositiveIntegerField(
        default=0, help_text="Post order in its series")
    created_date = models.DateTimeField(
        default=timezone.now, help_text="Creation date")
    modified_date = models.DateTimeField(
        auto_now=True, help_text="Last modification")
    published_date = models.DateTimeField(
        blank=True, null=True, help_text="Publication date")
    publication_state = models.CharField(
        max_length=25, verbose_name="Publication", choices=PUBLICATION_CHOICES, default='D',
        help_text="Post publication state")
    withdrawn = models.BooleanField(
        default=False, help_text="Is Post withdrawn")
    featuring_state = models.CharField(
        max_length=25, verbose_name="Featuring", choices=FEATURING_CHOICES, default='N', help_text="Featuring state")
    language = models.CharField(
        max_length=25, verbose_name="Language", choices=LANGUAGE_CHOICES, default='EN',
        help_text="What's the main language")
    is_outdated = models.BooleanField(
        default=False, help_text="Is Post content's outdated")
    url_to_article = models.URLField(
        default='', blank=True, help_text="Url to page that inspired the Post")
    url_to_article_title = models.CharField(
        max_length=200, default='', blank=True, help_text="What will be shown as url name")
    clicks = models.IntegerField(
        default=0, help_text="How many times the Post has been seen")
    history = HistoricalRecords()
    is_removed = models.BooleanField('is removed', default=False, db_index=True,
                                     help_text=('Soft delete'))
    enable_comments = models.BooleanField(default=True)

    objects = PostManager()

    class Meta:
        ordering = ['-published_date']
        get_latest_by = ['id']
        rules_permissions = {
            "add": rules.is_superuser,
            "update": rules.is_superuser,
        }

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            max_length = Post._meta.get_field('slug').max_length
            self.slug = orig = slugify(self.title)[:max_length]
            for x in itertools.count(2):
                if (
                    self.pk
                    and Post.objects.filter(Q(slug=self.slug),
                                            Q(author=self.author),
                                            Q(id=self.pk),
                                            ).exists()
                ):
                    break
                if not Post.objects.filter(slug=self.slug).exists():
                    break

                # Truncate & Minus 1 for the hyphen.
                self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        return super().save(*args, **kwargs)

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_absolute_update_url(self):
        return reverse('blog:post_edit', kwargs={'slug': self.slug})

    def get_absolute_delete_url(self):
        return reverse('blog:post_remove', kwargs={'slug': self.slug})

    def get_absolute_publish_url(self):
        return reverse('blog:post_publish', kwargs={'slug': self.slug})

    def get_absolute_publish_withdrawn_url(self):
        return reverse('blog:post_publish_withdrawn', kwargs={'slug': self.slug})

    def get_absolute_clone_url(self):
        return reverse('blog:clone_post', kwargs={'slug': self.slug})

    def get_absolute_admin_update_url(self):
        return reverse('admin:blog_post_change', kwargs={'object_id': self.pk})

    def is_published(self):
        """
        Return True if the event is publicly accessible.
        """
        return self.published_date <= timezone.now() and not self.withdrawn and not self.is_removed

    is_published.boolean = True

    def publish(self):
        self.published_date = timezone.now()
        self.publication_state = 'P'
        self.withdrawn = False
        self.save()

    def publish_withdrawn(self):
        self.published_date = timezone.now()
        self.publication_state = 'W'
        self.withdrawn = True
        self.save()

    def clicked(self):
        self.clicks += 1
        self.save_without_historical_record(update_fields=['clicks'])

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now

    def remove(self):
        self.is_removed = True
        self.save()

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.body)

    @property
    def author_name(self):
        return self.author.username

    @property
    def get_featured_cat(self):
        for post_cat in PostCatsLink.objects.filter(post_id=self.pk, category__is_removed=False,
                                                    featured_cat=True).select_related('post', 'category'):
            return post_cat

    @property
    def featured_cat_title(self):
        for post_cat in PostCatsLink.objects.filter(post_id=self.pk, category__is_removed=False,
                                                    featured_cat=True).select_related('post', 'category'):
            return post_cat.category

    def approved_comments(self):
        return self.comments.filter(approbation_state='AP')

    def removed_comments(self):
        return self.comments.filter(approbation_state='RE')

    def get_index_view_url(self):
        content_type = ContentType.objects.get_for_model(
            self.__class__)
        return reverse("%s:%s_list" % (content_type.app_label, content_type.model))


class PostContent(auto_prefetch.Model):
    post = auto_prefetch.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name="content")
    body = MarkdownxField(help_text="Post main content")
    body_image = models.ImageField(
        null=True, blank=True, upload_to='images/post/body_images/', help_text="Image in text")
    body_image_alt = models.CharField(
        default='', blank=True, max_length=200, help_text='Image in text'
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.post.title + '\'s Post Content'

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.body)


class Comment(auto_prefetch.Model):
    APPROBATION_CHOICES = [
        ('AP', 'Approved'),
        ('RE', 'Removed'),
    ]

    related_post = auto_prefetch.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='comments', help_text="Comment's related Post")
    author = models.CharField(
        max_length=200,
        default='',
        blank=True,
        help_text=(
            "You don't have to add one, the point of the Author being hiding who actually"
            ' wrote the comment by puttin another name, note that Admins and mods can still'
            ' find who wrote the comment'
        ),
    )
    author_logged = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="comment_author_logged",
        help_text="Comment author (a user with account)")
    title = models.CharField(
        max_length=200, default='', blank=True, help_text='Comment title'
    )
    body = models.TextField(verbose_name="Comment",
                            help_text="Comment main content")
    created_date = models.DateTimeField(
        default=timezone.now, help_text="Creation date")
    modified_date = models.DateTimeField(
        auto_now=True, help_text="Last modification")
    approbation_state = models.CharField(
        max_length=25, verbose_name="Approbation", choices=APPROBATION_CHOICES, default='AP',
        help_text="Comment approbation state")
    comment_answer = auto_prefetch.ForeignKey(
        'blog.Comment', on_delete=models.CASCADE, related_name='related_comment', null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.full_title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.related_post.slug}) + f'#comment-{self.pk}'

    @property
    def full_title(self):
        full_t = self.related_post.title + ' - '
        if self.title:
            full_t = full_t + self.title + ' - '
        full_t = full_t + self.body
        return full_t

    def approve(self):
        self.approbation_state = 'AP'
        self.save()

    def remove(self):
        self.approbation_state = 'RE'
        self.save()
