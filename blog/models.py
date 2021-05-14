import rules
import datetime
import auto_prefetch
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from rules.contrib.models import RulesModelBase, RulesModelMixin

from simple_history.models import HistoricalRecords
from taggit.managers import TaggableManager


class Category(RulesModelMixin, auto_prefetch.Model, metaclass=RulesModelBase):
    title = models.CharField(max_length=200, help_text="Category title")
    description = models.TextField(
        blank=True, help_text="Category description")
    slug = models.SlugField(unique=True, default="",
                            max_length=200, help_text="Category slug")
    withdrawn = models.BooleanField(
        default=False, help_text="Is Category withdrawn")
    history = HistoricalRecords()

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


class Series(RulesModelMixin, auto_prefetch.Model, metaclass=RulesModelBase):
    title = models.CharField(max_length=200, help_text="Series title")
    description = models.TextField(blank=True, help_text="Series description")
    slug = models.SlugField(unique=True, default="",
                            max_length=200, help_text="Series slug")
    withdrawn = models.BooleanField(
        default=False, help_text="Is Series withdrawn")
    history = HistoricalRecords()

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


class PostCatsLink(auto_prefetch.Model):
    post = auto_prefetch.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='post_to_category')
    category = auto_prefetch.ForeignKey(
        'blog.Category', on_delete=models.CASCADE, related_name='category_to_post')
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
        max_length=200, default='', blank=True, help_text="Featured post title")
    body = MarkdownxField(help_text="Post main content", blank=True)
    post_image = models.ImageField(
        null=True, blank=True, upload_to='images/post/', help_text="Post image")
    description = models.TextField(help_text="Post description")
    slug = models.SlugField(unique=True, max_length=200, help_text="Post slug")
    categories = models.ManyToManyField(
        'blog.Category', through='PostCatsLink', help_text="Post categories")
    tags = TaggableManager(blank=True)
    series = auto_prefetch.ForeignKey(
        'blog.Series', on_delete=models.CASCADE, related_name="post_series",  help_text="Post series", blank=True, null=True)
    post_order_in_series = models.PositiveIntegerField(
        default=0, help_text="Post order in its series")
    created_date = models.DateTimeField(
        default=timezone.now, help_text="Creation date")
    modified_date = models.DateTimeField(
        auto_now=True, help_text="Last modification")
    published_date = models.DateTimeField(
        blank=True, null=True, help_text="Publication date")
    publication_state = models.CharField(
        max_length=25, verbose_name="Publication", choices=PUBLICATION_CHOICES, default='D', help_text="Post publication state")
    withdrawn = models.BooleanField(
        default=False, help_text="Is Post withdrawn")
    featuring_state = models.CharField(
        max_length=25, verbose_name="Featuring", choices=FEATURING_CHOICES, default='N', help_text="Featuring state")
    language = models.CharField(
        max_length=25, verbose_name="Language", choices=LANGUAGE_CHOICES, default='EN', help_text="What's the main language")
    url_post_type = models.URLField(
        default='', blank=True, help_text="Url to page that inspired the Post")
    url_post_type_name = models.CharField(
        max_length=200, default='', blank=True, help_text="What will be shown as url name")
    clicks = models.IntegerField(
        default=0, help_text="How many times the Post has been seen")
    history = HistoricalRecords()
    enable_comments = models.BooleanField(default=True)

    class Meta:
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

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

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

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.body)

    def approved_comments(self):
        return self.comments.filter(approbation_state='AP')

    def removed_comments(self):
        return self.comments.filter(approbation_state='RE')


class PostContent(auto_prefetch.Model):
    post = auto_prefetch.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name="content")
    body = MarkdownxField(help_text="Post main content")
    post_body_image = models.ImageField(
        null=True, blank=True, upload_to='images/post/body_images/', help_text="Image in text")
    post_body_image_alt = models.CharField(
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
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="comment_author_logged", help_text="Comment author (a user with account)")
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
        max_length=25, verbose_name="Approbation", choices=APPROBATION_CHOICES, default='AP', help_text="Comment approbation state")
    comment_answer = auto_prefetch.ForeignKey(
        'blog.Comment', on_delete=models.CASCADE, related_name='related_comment', null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.fulltitle

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.related_post.slug}) + f'#comment-{self.pk}'

    @property
    def fulltitle(self):
        if self.author_logged and self.author:
            author_in_name = f'{self.author_logged} - {self.author}'
        elif self.author_logged:
            author_in_name = self.author_logged
        else:
            author_in_name = self.author
        if self.title:
            name = f'{self.related_post.title} - {self.title} - {author_in_name}'
        else:
            name = f'{self.related_post.title} - {author_in_name}'
        return name

    def approve(self):
        self.approbation_state = 'AP'
        self.save()

    def remove(self):
        self.approbation_state = 'RE'
        self.save()
