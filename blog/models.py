import datetime
from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(unique=True, default="")
    withdrawn = models.BooleanField(default=False)

    class Meta:
        ordering = ['pk']
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_category_list', kwargs={'slug': self.slug})


class PostCatsLink(models.Model):
    post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='post_to_category')
    category = models.ForeignKey(
        'blog.Category', on_delete=models.CASCADE, related_name='category_to_post')
    featured_cat = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Post to Category Link"

    def __str__(self):
        return '%s - %s' % (self.post.title, self.category.name)


class Post(models.Model):
    PUBLICATION_CHOICES = [
        ('P', 'Published'),
        ('W', 'Withdrawn'),
        ('D', 'Draft'),
    ]

    FEATURING_CHOICES = [
        ('F', 'Featured'),
        ('B', 'Big'),
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

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="post_author")
    title = models.CharField(max_length=200)
    featured_title = models.CharField(max_length=200, default='', blank=True)
    body = MarkdownxField()
    post_image = models.ImageField(
        null=True, blank=True, upload_to='images/post/')
    description = models.TextField()
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(
        'blog.Category', through='PostCatsLink')
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    publication_state = models.CharField(
        max_length=25, verbose_name="Publication", choices=PUBLICATION_CHOICES, default='D')
    withdrawn = models.BooleanField(default=False)
    featuring_state = models.CharField(
        max_length=25, verbose_name="Featuring", choices=FEATURING_CHOICES, default='N')
    featured = models.BooleanField(default=False)
    big = models.BooleanField(default=False)
    language = models.CharField(
        max_length=25, verbose_name="Language", choices=LANGUAGE_CHOICES, default='EN')
    url_post_type = models.URLField(default='', blank=True)
    url_post_type_name = models.CharField(
        max_length=200, default='', blank=True)
    clicks = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

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
        self.save(update_fields=['clicks'])

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


class Comment(models.Model):
    APPROBATION_CHOICES = [
        ('AP', 'Approved'),
        ('RE', 'Removed'),
    ]

    related_post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='comments')
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
    author_logged = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="comment_author_logged")
    message = models.TextField(verbose_name="Comment")
    created_date = models.DateTimeField(default=timezone.now)
    approbation_state = models.CharField(
        max_length=25, verbose_name="Approbation", choices=APPROBATION_CHOICES, default='AP')
    comment_answer = models.ForeignKey(
        'blog.Comment', on_delete=models.CASCADE, related_name='related_comment', null=True, blank=True)

    def __str__(self):
        if self.author_logged:
            author_in_name = self.author_logged
        else:
            author_in_name = self.author
        return '%s - %s - %s' % (self.related_post.title, author_in_name, self.pk)

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.related_post.slug})

    def approve(self):
        self.approbation_state = 'AP'
        self.save()

    def remove(self):
        self.approbation_state = 'RE'
        self.save()
