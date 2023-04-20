import datetime
import itertools
import re

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google
from django.db import models
from django.db.models import F, Q
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html, mark_safe

import auto_prefetch
import rules
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from rules.contrib.models import RulesModelBase, RulesModelMixin
from simple_history.models import HistoricalRecords
from taggit_selectize.managers import TaggableManager

from custom_taggit.models import CustomTaggedItem

from .managers import CategoryManager, PostManager, SeriesManager
from .utils import generate_unique_vanity


class Category(RulesModelMixin, auto_prefetch.Model, metaclass=RulesModelBase):
    """Category model

    A model for Category

    Args:
        RulesModelMixin ([type]): [description]
        auto_prefetch ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to RulesModelBase.

    Returns:
        Category: A model for Category
    """

    parent = auto_prefetch.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="category_children",
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=200, help_text="Category title")
    suffix = models.CharField(max_length=200, help_text="Category suffix", blank=True, default="")
    description = models.TextField(blank=True, help_text="Category description")
    slug = models.SlugField(unique=True, default="", max_length=200, help_text="Category slug")
    created_date = models.DateTimeField(default=timezone.now, help_text="Creation date")
    mod_date = models.DateTimeField(auto_now=True, help_text="Last modification")
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")
    withdrawn = models.BooleanField(default=False, help_text="Is Category withdrawn")
    needs_reviewing = models.BooleanField(default=False, help_text=("Needs reviewing"))
    history = HistoricalRecords()

    objects: CategoryManager = CategoryManager()

    class Meta(auto_prefetch.Model.Meta):
        """Meta class for Category Model"""

        ordering = ["pk"]
        verbose_name_plural = "Categories"
        rules_permissions = {
            "add": rules.is_superuser,
            "update": rules.is_superuser,
        }

    def __str__(self):
        """String representation of Category"""
        return self.full_title

    def save(self, *args, **kwargs):
        """Save Category"""
        try:
            ping_google()
        except Exception:  # skipcq: PYL-W0703
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
        if not self.slug:
            self.slug = slugify(self.full_title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute url for this category"""
        return reverse("blog:post_category_list", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        """Get the update url for this category"""
        return reverse("blog:category_edit", kwargs={"slug": self.slug})

    def get_absolute_needs_review_url(self):
        """Get the needs review url for this category"""
        return reverse("blog:category_needs_review", kwargs={"slug": self.slug})

    def get_absolute_delete_url(self):
        """Get the delete url for this category"""
        return reverse("blog:category_remove", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get the admin update url for this category"""
        return reverse("admin:blog_category_change", kwargs={"object_id": self.pk})

    def needs_review(self):
        """Set the needs_review flag for this category"""
        self.needs_reviewing = True
        self.save()

    def soft_delete(self):
        """Soft delete Category"""
        self.deleted_at = timezone.now()
        self.save()

    @property
    def get_post_count(self):
        """Get the number of posts in this category"""
        return self.postcatslink_set.filter(
            post__pub_date__lte=timezone.now(),
            post__withdrawn=False,
            post__deleted_at=None,
        ).count()

    @property
    def get_superuser_post_count(self):
        """Get the number of posts in this category"""
        return self.postcatslink_set.filter(post__deleted_at=None).count()

    @property
    def get_superuser_percent_of_posts(self) -> str:
        """Get the percentage of posts in this category"""
        percentage = self.get_superuser_post_count / Post.objects.filter(deleted_at=None).count() * 100
        return f"{round(percentage, 2)}%"

    @property
    def get_percent_of_posts(self) -> str:
        """Get the percentage of posts in this category"""
        percentage = (
            self.get_post_count
            / Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None).count()
            * 100
        )
        return f"{round(percentage, 2)}%"

    @property
    def full_title(self) -> str:
        """Get the full title of the category"""
        full_title = ""
        if self.suffix:
            full_title = self.title + " " + self.suffix
        elif not self.suffix and not self.parent:
            full_title = self.title
        elif not self.suffix and self.parent and self.parent.suffix:
            full_title = self.title + " " + self.parent.suffix
        else:
            full_title = self.title
        return full_title

    def get_index_view_url(self):
        """Get the index view url for this category"""
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f"{content_type.app_label}:{content_type.model}_list")


class Series(RulesModelMixin, auto_prefetch.Model, metaclass=RulesModelBase):
    """Series Model

    A model for Series

    Args:
        RulesModelMixin ([type]): [description]
        auto_prefetch ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to RulesModelBase.

    Returns:
        Series: A model for Series
    """

    title = models.CharField(max_length=200, help_text="Series title")
    description = models.TextField(blank=True, help_text="Series description")
    slug = models.SlugField(unique=True, default="", max_length=200, help_text="Series slug")
    created_date = models.DateTimeField(default=timezone.now, help_text="Creation date")
    mod_date = models.DateTimeField(auto_now=True, help_text="Last modification")
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")
    withdrawn = models.BooleanField(default=False, help_text="Is Series withdrawn")
    needs_reviewing = models.BooleanField(default=False, help_text=("Needs reviewing"))
    history = HistoricalRecords()

    objects: SeriesManager = SeriesManager()

    class Meta(auto_prefetch.Model.Meta):
        """Meta class for Series Model"""

        rules_permissions = {
            "add": rules.is_superuser,
            "update": rules.is_superuser,
        }
        ordering = ["pk"]
        verbose_name_plural = "Series"

    def __str__(self):
        """String representation of Series"""
        return self.title

    def save(self, *args, **kwargs):
        """Save Series"""
        try:
            ping_google()
        except Exception:  # skipcq: PYL-W0703
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Get the absolute url for this Series"""
        return reverse("blog:post_series_list", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        """Get the absolute url for this Series"""
        return reverse("blog:series_edit", kwargs={"slug": self.slug})

    def get_absolute_needs_review_url(self):
        """Get the absolute url for this Series"""
        return reverse("blog:series_needs_review", kwargs={"slug": self.slug})

    def get_absolute_delete_url(self):
        """Get the absolute url for this Series"""
        return reverse("blog:series_remove", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get the absolute url for this Series"""
        return reverse("admin:blog_series_change", kwargs={"object_id": self.pk})

    def needs_review(self):
        """Set this Series to needs reviewing"""
        self.needs_reviewing = True
        self.save()

    def soft_delete(self):
        """Soft delete Series"""
        self.deleted_at = timezone.now()
        self.save()

    @property
    def get_post_count(self):
        """Get the number of posts in this series"""
        return self.post_series.filter(
            pub_date__lte=timezone.now(),
            withdrawn=False,
            deleted_at=None,
        ).count()

    @property
    def get_superuser_post_count(self):
        """Get the number of posts in this series"""
        return self.post_series.filter(deleted_at=None).count()

    @property
    def get_superuser_percent_of_posts(self) -> str:
        """Get the percentage of posts in this series"""
        percentage = self.get_superuser_post_count / Post.objects.filter(deleted_at=None).count() * 100
        return f"{round(percentage, 2)}%"

    @property
    def get_percent_of_posts(self) -> str:
        """Get the percentage of posts in this series"""
        percentage = (
            self.get_post_count
            / Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None).count()
            * 100
        )
        return f"{round(percentage, 2)}%"

    def get_index_view_url(self):
        """Get the index view url for this Series"""
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f"{content_type.app_label}:{content_type.model}_list")


class PostCatsLink(auto_prefetch.Model):
    """PostCatsLink Through Table Model

    A through table Model linking Post and Category

    Args:
        auto_prefetch ([type]): [description]

    Returns:
        PostCatsLink: postcatslink_set
    """

    post = auto_prefetch.ForeignKey("blog.Post", on_delete=models.CASCADE)
    category = auto_prefetch.ForeignKey("blog.Category", on_delete=models.CASCADE)
    featured_cat = models.BooleanField(default=False)

    class Meta(auto_prefetch.Model.Meta):
        """Meta class for PostCatsLink Through Table"""

        verbose_name_plural = "Post to Category Link"

    def __str__(self):
        """String representation of PostCatsLink"""
        return f"{self.post.title} - {self.category.title}"


class Post(RulesModelMixin, auto_prefetch.Model, metaclass=RulesModelBase):
    """Post Model

    A model for Blog Posts

    Args:
        RulesModelMixin ([type]): [description]
        auto_prefetch ([type]): [description]
        metaclass ([type], optional): [description]. Defaults to RulesModelBase.

    Returns:
        Post: A model for Post
    """

    PUBLICATION_CHOICES = [
        ("P", "Published"),
        ("W", "Withdrawn"),
        ("D", "Draft"),
    ]

    FEATURING_CHOICES = [
        ("F", "Featured"),
        ("SF", "Super Featured"),
        ("N", "Not Featured"),
    ]

    LANGUAGE_CHOICES = [
        ("EN", "English"),
        ("FR", "Français"),
        ("DE", "Deutsch"),
        ("ML", "Multi Linguistic"),
        ("OL", "Other Language"),
        ("NS", "Not Specified"),
    ]

    author = auto_prefetch.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_author",
        help_text="Post author",
    )
    title = models.CharField(max_length=200, help_text="Post title")
    featured_title = models.CharField(max_length=27, default="", blank=True, help_text="Featured post title")
    body = MarkdownxField(help_text="Post main content", blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/post/", help_text="Post image")
    description = models.TextField(help_text="Post description")
    slug = models.SlugField(unique=True, max_length=200, help_text="Post slug")
    categories = models.ManyToManyField("blog.Category", through="PostCatsLink", help_text="Post categories")
    tags = TaggableManager(blank=True, through=CustomTaggedItem)
    series = auto_prefetch.ForeignKey(
        "blog.Series",
        on_delete=models.CASCADE,
        related_name="post_series",
        help_text="Post series",
        blank=True,
        null=True,
    )
    order_in_series = models.PositiveIntegerField(default=0, help_text="Post order in its series")
    created_date = models.DateTimeField(default=timezone.now, help_text="Creation date")
    mod_date = models.DateTimeField(auto_now=True, help_text="Last modification")
    pub_date = models.DateTimeField(blank=True, null=True, help_text="Publication date")
    deleted_at = models.DateTimeField(blank=True, null=True, help_text="Deletion date for soft delete")
    publication_state = models.CharField(
        max_length=25,
        verbose_name="Publication",
        choices=PUBLICATION_CHOICES,
        default="D",
        help_text="Post publication state",
    )
    withdrawn = models.BooleanField(default=False, help_text="Is Post withdrawn")
    featuring_state = models.CharField(
        max_length=25,
        verbose_name="Featuring",
        choices=FEATURING_CHOICES,
        default="N",
        help_text="Featuring state",
    )
    language = models.CharField(
        max_length=25,
        verbose_name="Language",
        choices=LANGUAGE_CHOICES,
        default="EN",
        help_text="What's the main language",
    )
    url_to_article = models.URLField(default="", blank=True, help_text="Url to page that inspired the Post")
    url_to_article_title = models.CharField(
        max_length=200,
        default="",
        blank=True,
        help_text="What will be shown as url name",
    )
    clicks = models.IntegerField(default=0, help_text="How many times the Post has been seen")
    rnd_choice = models.IntegerField(default=0, help_text="How many times the Post has been randomly chosen")
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="post_likes", blank=True)
    is_content_outdated = models.TextField(default="", blank=True, help_text="Is Post content's outdated")
    is_content_outdated_date = models.DateTimeField(blank=True, null=True, help_text="Outdated date")
    needs_reviewing = models.BooleanField(default=False, help_text=("Needs reviewing"))
    enable_comments = models.BooleanField(default=True)
    vanity_url = models.CharField(max_length=200, default="", blank=True, help_text="Vanity url for the Post")
    history = HistoricalRecords()

    objects: PostManager = PostManager()

    class Meta(auto_prefetch.Model.Meta):
        """Meta class for Post Model"""

        ordering = ["-pub_date"]
        get_latest_by = ["id"]
        rules_permissions = {
            "add": rules.is_superuser,
            "update": rules.is_superuser,
        }

    def __str__(self):
        """String representation of Post"""
        return self.title

    def save(self, *args, **kwargs):
        """Save Post"""
        try:
            ping_google()
        except Exception:  # skipcq: PYL-W0703
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
        if not self.vanity_url:
            self.vanity_url = generate_unique_vanity(5, 10, Post)
        if not self.slug:
            max_length = Post._meta.get_field("slug").max_length
            self.slug = orig = slugify(self.title)[:max_length]
            for x in itertools.count(2):
                if (
                    self.pk
                    and Post.objects.filter(
                        Q(slug=self.slug),
                        Q(author=self.author),
                        Q(id=self.pk),
                    ).exists()
                ):
                    break
                if not Post.objects.filter(slug=self.slug).exists():
                    break

                # Truncate & Minus 1 for the hyphen.
                self.slug = f"{orig[: max_length - len(str(x)) - 1]}-{x}"
        return super().save(*args, **kwargs)

    def save_without_historical_record(self, *args, **kwargs):
        """Save Post without Historical Record"""
        self.skip_history_when_saving = True  # skipcq: PYL-W0201
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

    def get_absolute_url(self):
        """Get absolute url of Post"""
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def get_absolute_update_url(self):
        """Get absolute url of Post update"""
        return reverse("blog:post_edit", kwargs={"slug": self.slug})

    def get_absolute_outdated_url(self):
        """Get absolute url of Post is outdated"""
        return reverse("blog:post_is_outdated", kwargs={"slug": self.slug})

    def get_absolute_needs_review_url(self):
        """Get absolute url of Post needs review"""
        return reverse("blog:post_needs_review", kwargs={"slug": self.slug})

    def get_absolute_delete_url(self):
        """Get absolute url of Post delete"""
        return reverse("blog:post_remove", kwargs={"slug": self.slug})

    def get_absolute_publish_url(self):
        """Get absolute url of Post publish"""
        return reverse("blog:post_publish", kwargs={"slug": self.slug})

    def get_absolute_publish_withdrawn_url(self):
        """Get absolute url of Post publish"""
        return reverse("blog:post_publish_withdrawn", kwargs={"slug": self.slug})

    def get_absolute_clone_url(self):
        """Get absolute url of Post clone"""
        return reverse("blog:clone_post", kwargs={"slug": self.slug})

    def get_absolute_admin_update_url(self):
        """Get absolute url of Post admin update"""
        return reverse("admin:blog_post_change", kwargs={"object_id": self.pk})

    def get_absolute_define_featured_category_url(self):
        """Get absolute url to define a featured category to a post"""
        return reverse("blog:post_define_featured_category", kwargs={"slug": self.slug})

    def get_absolute_like_url(self):
        """Get absolute url to like a post"""
        return reverse("blog:post_like", kwargs={"slug": self.slug})

    def get_absolute_dislike_url(self):
        """Get absolute url to dislike a post"""
        return reverse("blog:post_dislike", kwargs={"slug": self.slug})

    def publish(self):
        """Publish Post"""
        self.pub_date = timezone.now()
        self.publication_state = "P"
        self.withdrawn = False
        self.save()

    def publish_withdrawn(self):
        """Publish Post Withdrawn"""
        self.pub_date = timezone.now()
        self.publication_state = "W"
        self.withdrawn = True
        self.save()

    def needs_review(self):
        """Needs Review Post"""
        self.needs_reviewing = True
        self.save()

    def clicked(self):
        """Clicked Post"""
        self.clicks = F("clicks") + 1
        self.save_without_historical_record(update_fields=["clicks"])

    def rnd_chosen(self):
        """Rnd Chosen Post"""
        self.rnd_choice = F("rnd_choice") + 1
        self.save_without_historical_record(update_fields=["rnd_choice"])

    def was_published_recently(self):
        """Was published recently Post"""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def soft_delete(self):
        """Soft delete Post"""
        self.deleted_at = timezone.now()
        self.save()

    @property
    def is_scheduled(self) -> bool:
        """Is Scheduled Post"""
        now = timezone.now()
        if not self.pub_date:
            return False

        return self.pub_date >= now

    @property
    def author_name(self):
        """Author Name Post"""
        return self.author.username

    @property
    def get_tags(self):
        """Get Tags Post"""
        return self.tags.filter(withdrawn=False)

    @property
    def get_admin_tags(self):
        """Get Admin Tags Post"""
        return self.tags.all()

    @property
    def has_code(self) -> bool:
        """Post has code"""
        return self.tags.filter(slug="has-code").exists()

    @property
    def is_wednesday(self, slug: str) -> bool:
        """Post has category"""
        return self.categories.filter(slug="wednesday").exists()

    @property
    def get_featured_cat(self):
        """Get Featured Cat Post"""
        for post_cat in PostCatsLink.objects.filter(
            post_id=self.pk, category__deleted_at=None, featured_cat=True
        ).select_related("post", "category"):
            return post_cat

    @property
    def featured_cat_title(self):
        """Featured Cat Title Post"""
        for post_cat in PostCatsLink.objects.filter(
            post_id=self.pk, category__deleted_at=None, featured_cat=True
        ).select_related("post", "category"):
            return post_cat.category.full_title

    @property
    def get_category_count(self) -> int:
        """Get Category Count"""
        return PostCatsLink.objects.filter(post_id=self.pk, category__deleted_at=None).count()

    # Property that gets the first line of body field
    @property
    def first_line(self):
        """First Line Post"""
        return self.body.split("\n")[0]

    # Property that removes anything between ![] in the first line
    @property
    def first_line_no_img(self):
        """First Line No Img Post"""
        return re.sub(r"!\[.*?\]", "", self.first_line)

    # Property that gets everything after the first line
    @property
    def after_first_line(self):
        """After First Line Post"""
        return self.body.split("\n")[1:]

    # Property that adds "This post is outdated" just after the first line
    @property
    def first_line_outdated(self):
        """First Line Outdated Post"""
        return format_html(
            '<div class="admonition outdated">'
            '<p class="admonition-title">This post is outdated as of {0}</p>'
            "<p>{1}</p></div>",
            self.is_content_outdated_date.strftime("%Y-%m-%d"),
            mark_safe(self.is_content_outdated),  # skipcq: BAN-B308
        )

    # Property that adds the post image just after the title
    @property
    def first_line_image(self):
        """First Line Image Post"""
        return format_html(
            '<img src="{0}" alt="{1}">',
            self.image.url,
            self.title,
        )

    # Property that defines the body_content depending on if it's outdated or not
    @property
    def body_content(self):
        """Body Content Post"""
        body = self.body
        if self.is_content_outdated_date is not None or self.image is not None:
            body = self.first_line
            body += "\n"
        if self.is_content_outdated_date is not None:
            body += self.first_line_outdated
        if self.image:
            body += self.first_line_image
        body += "\n".join(self.after_first_line)
        return body

    # Create a property that returns the markdown instead
    @property
    def formatted_markdown(self):
        """Formatted Markdown Post"""
        return markdownify(self.body_content)

    # Property that returns the number of likes
    @property
    def total_likes(self):
        """Likes Post"""
        return self.likes.count()

    def get_index_view_url(self):
        """Get Index View Url Post"""
        content_type = ContentType.objects.get_for_model(self.__class__)
        return reverse(f"{content_type.app_label}:{content_type.model}_list")
