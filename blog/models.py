from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from django.db.models import Q

import itertools


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    private = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:post_category_list', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class PostCatsLink(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    category = models.ForeignKey('blog.Category', on_delete=models.CASCADE)
    featured_cat = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.category.name)


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    featured_title = models.CharField(
        max_length=200, null=True, unique=False, blank=True)
    body = MarkdownxField()
    post_image = models.ImageField(
        null=True, blank=True, upload_to='images/post/')
    description = models.TextField()
    slug = models.SlugField(null=False, unique=True)
    categories = models.ManyToManyField(
        'blog.Category', related_name='cat', through='PostCatsLink')
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)
    private = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    big = models.BooleanField(default=False)
    url_post_type = models.URLField(null=True, blank=True)
    url_post_type_name = models.CharField(
        max_length=200, null=True, blank=True)
    clicks = models.IntegerField(default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def publish_private(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def clicked(self):
        self.clicks += 1
        self.save()

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def _get_next_or_previous_by_slug(self, field, is_next, **kwargs):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        max_length = Post._meta.get_field('slug').max_length
        self.slug = orig = slugify(self.title)[:max_length]
        for x in itertools.count(2):
            if self.pk:
                if Post.objects.filter(Q(slug=self.slug),
                                       Q(author=self.author),
                                       Q(id=self.pk),
                                       ).exists():
                    break
            if not Post.objects.filter(slug=self.slug).exists():
                break

            # Truncate & Minus 1 for the hyphen.
            self.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        return super().save(*args, **kwargs)

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        return markdownify(self.body)

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def removed_comments(self):
        return self.comments.filter(removed_comment=True)

    # def get_categories(self):
    #     return [p.name for p in self.categories.all()]


class Comment(models.Model):
    related_post = models.ForeignKey(
        'blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(
        max_length=200, null=True, blank=True,
        help_text="You don't have to add one, the point of the Author being hiding who actually wrote the comment by puttin another name, note that Admins and mods can still find who wrote the comment")
    author_logged = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(verbose_name="Comment")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=True)
    removed_comment = models.BooleanField(default=False)
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
        self.approved_comment = True
        self.save()

    def remove(self):
        self.removed_comment = True
        self.save()
