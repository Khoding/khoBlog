from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView
from django.views.generic.dates import (
    ArchiveIndexView,
    DateDetailView,
    DayArchiveView,
    MonthArchiveView,
    TodayArchiveView,
    WeekArchiveView,
    YearArchiveView,
)

from rules.contrib.views import AutoPermissionRequiredMixin

from blog.filters import PostFilter
from custom_taggit.forms import TagForm
from custom_taggit.models import CustomTag
from khoBlog.utils.superuser_required import superuser_required

from .forms import (
    CategoryCreateForm,
    CategoryDeleteForm,
    CategoryEditForm,
    PostCloneForm,
    PostCreateForm,
    PostDeleteForm,
    PostEditForm,
    SeriesCreateForm,
    SeriesDeleteForm,
    SeriesEditForm,
)
from .models import Category, Post, PostContent, Series


class PostListView(ListView):
    """PostListView List View

    The default List View for Posts

    Args:
        ListView (ListView): Lists elements

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = "blog/lists/post_list.html"
    context_object_name = "posts"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        query = PostFilter(
            self.request.GET,
            queryset=Post.objects.filter(Q(pub_date__lte=timezone.now(), withdrawn=False)),
        )
        if query is not None and query != "":
            return query.qs
        return Post.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Latest Posts"
        context["show_featured"] = True
        context["filter_form"] = PostFilter()
        return context


class WeblogTemplateView(TemplateView):
    """WeblogTemplateView TemplateView

    An alternative List View for Posts

    Args:
        TemplateView (TemplateView): A List View

    Returns:
        posts: A list of posts
    """

    template_name = "blog/lists/weblog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Weblog"
        return context


class PostInCategoryListView(ListView):
    """PostInCategoryListView List View

    Lists all Posts in a particular Category

    Args:
        ListView (ListView): A list View

    Raises:
        PermissionDenied: If the currently logged in user doesn't have access to the requested Category

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = "blog/lists/post_category_list.html"
    context_object_name = "posts"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        if not self.category.withdrawn or self.request.user.is_superuser:
            self.title = self.category.title
            self.description = self.category.description
        else:
            raise PermissionDenied
        return self.model.objects.get_common_queryset(self.request.user).filter(categories=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cats"] = self.category
        context["title"] = self.title
        context["description"] = self.description
        return context


class PostInSeriesListView(ListView):
    """PostInSeriesListView List View

    Lists all Posts in a particular Series

    Args:
        ListView (ListView): A list View

    Raises:
        PermissionDenied: If the currently logged in user doesn't have access to the requested Series

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = "blog/lists/post_series_list.html"
    context_object_name = "posts"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        self.series = get_object_or_404(Series, slug=self.kwargs["slug"])
        if not self.series.withdrawn or self.request.user.is_superuser:
            self.title = self.series.title
            self.description = self.series.description
        else:
            raise PermissionDenied
        return (
            self.model.objects.get_common_queryset(self.request.user)
            .filter(series=self.series)
            .order_by("order_in_series")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["series"] = self.series
        context["title"] = self.series.title
        context["description"] = self.description
        return context


class CategoryListView(ListView):
    """CategoryListView ListView

    A list of Categories

    Args:
        ListView ([type]): [description]

    Returns:
        category_list: A list of Categories
    """

    model = Category
    template_name = "blog/lists/category_list.html"
    context_object_name = "category_list"
    paginate_by = 20
    paginate_orphans = 5
    ordering = "pk"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.get_without_removed()
        return self.model.objects.filter(withdrawn=False).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Category List"
        context["description"] = "List of categories"
        context["content_type"] = "category"
        return context


class SeriesListView(ListView):
    """SeriesListView ListView

    A list of Series

    Args:
        ListView ([type]): [description]

    Returns:
        series_list: A list of Series
    """

    model = Series
    template_name = "blog/lists/series_list.html"
    context_object_name = "series_list"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.get_without_removed()
        return self.model.objects.filter(withdrawn=False).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Series List"
        context["description"] = "List of series"
        context["content_type"] = "series"
        return context


class PostDetailView(DetailView):
    """PostDetailView DetailView

    A view showing the Details of a Post

    Args:
        DetailView ([type]): [description]

    Raises:
        PermissionDenied: Post is removed
        PermissionDenied: User doesn't have access to requested Post

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = "blog/post_detail.html"

    def get_queryset(self):
        self.post = get_object_or_404(Post, slug=self.kwargs["slug"])
        self.post.clicked()
        if self.post.is_removed:
            raise PermissionDenied
        if self.request.user.is_superuser:
            self.series = (
                self.model.objects.get_queryset()
                .filter(series__isnull=False, series=self.post.series)
                .order_by("order_in_series")
            )
            self.title = self.post.title
            self.description = self.post.description
            if self.post.pub_date:
                self.prev_post = (
                    Post.objects.filter(pub_date__lt=self.post.pub_date, is_removed=False)
                    .exclude(pk=self.post.pk)
                    .order_by("-pub_date")
                    .first()
                )
                self.next_post = (
                    Post.objects.filter(pub_date__gt=self.post.pub_date, is_removed=False)
                    .exclude(pk=self.post.pk)
                    .order_by("pub_date")
                    .first()
                )
            else:
                self.prev_post = (
                    Post.objects.filter(created_date__lt=self.post.created_date, is_removed=False)
                    .exclude(pk=self.post.pk)
                    .order_by("-created_date")
                    .first()
                )
                self.next_post = (
                    Post.objects.filter(created_date__gt=self.post.created_date, is_removed=False)
                    .exclude(pk=self.post.pk)
                    .order_by("created_date")
                )
            if self.next_post == self.post:
                self.next_post = ""
            if self.prev_post == self.post:
                self.prev_post = ""
        else:
            self.series = (
                self.model.objects.get_queryset()
                .filter(series__isnull=False, series=self.post.series)
                .order_by("order_in_series")
            )
            if self.post.withdrawn or not self.post.pub_date or self.post.pub_date >= timezone.now():
                raise PermissionDenied
            self.title = self.post.title
            self.description = self.post.description
            self.prev_post = (
                Post.objects.filter(
                    pub_date__lt=self.post.pub_date,
                    pub_date__lte=timezone.now(),
                    withdrawn=False,
                    is_removed=False,
                )
                .exclude(pk=self.post.pk)
                .order_by("-pub_date")
                .first()
            )
            self.next_post = (
                Post.objects.filter(
                    pub_date__gt=self.post.pub_date,
                    pub_date__lte=timezone.now(),
                    withdrawn=False,
                    is_removed=False,
                )
                .exclude(pk=self.post.pk)
                .order_by("pub_date")
                .first()
            )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_base_common_queryset()
        context["series"] = self.series
        context["title"] = self.title
        context["description"] = self.description
        context["similar_posts"] = self.tags = self.post.tags.similar_objects()[:5]
        context["comment_next"] = self.post.get_absolute_url()
        context["next_post"] = self.next_post
        context["prev_post"] = self.prev_post
        return context


def redirect_to_latest(request):
    if request.user.is_superuser:
        latest = Post.objects.latest()
    else:
        latest = Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, is_removed=False).latest()
    return redirect(reverse("blog:post_detail", args=(latest.slug,)))


def redirect_to_random(request):
    if request.user.is_superuser:
        post = Post.objects.filter(is_removed=False).order_by("?")[0]
    else:
        post = Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, is_removed=False).order_by("?")[0]
    post.rnd_chosen()
    return redirect(reverse("blog:post_detail", args=(post.slug,)))


def post_detail_through_id(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return redirect(reverse("blog:post_detail", args=(post.slug,)))


@superuser_required()
class PostDraftListView(ListView):
    """PostDraftListView ListView

    Lists Draft Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = "blog/lists/post_draft_list.html"
    context_object_name = "posts"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        return self.model.objects.filter(pub_date__isnull=True).order_by("-created_date").get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Drafts"
        context["description"] = "List of draft posts"
        return context


@superuser_required()
class PostScheduledListView(ListView):
    """PostScheduledListView ListView

    Lists Scheduled Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = "blog/lists/post_scheduled_list.html"
    context_object_name = "posts"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        return (
            self.model.objects.filter(pub_date__gte=timezone.now(), withdrawn=False)
            .get_without_removed()
            .order_by("pub_date")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Scheduled"
        context["description"] = "List of scheduled posts"
        return context


@superuser_required()
class PostWithdrawnListView(ListView):
    """PostWithdrawnListView ListView

    Lists Withdrawn Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = "blog/lists/post_withdrawn_list.html"
    context_object_name = "posts"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        return self.model.objects.filter(withdrawn=True).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Withdrawn"
        context["description"] = "List of withdrawn posts"
        return context


class TagListView(ListView):
    """TagListView ListView

    List of Tags

    Args:
        ListView ([type]): [description]

    Returns:
        tags: A list of tags
    """

    model = CustomTag
    template_name = "blog/lists/tag_list.html"
    context_object_name = "tags"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.model.objects.all()
        return self.model.objects.filter(withdrawn=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Tag List"
        context["description"] = "List of all tags"
        context["content_type"] = "tag"
        return context


class PostWithTagListView(ListView):
    """PostWithTagListView ListView

    Lists all Posts tagged with a given Tag

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    model = Post
    template_name = "blog/lists/post_list.html"
    context_object_name = "posts"
    paginate_by = 20
    paginate_orphans = 5

    def get_queryset(self):
        self.tags = get_object_or_404(CustomTag, slug=self.kwargs["slug"])
        self.title = f"Tag: {self.tags.name}"
        self.description = f"Posts tagged with {self.tags.name}"
        return self.model.objects.get_common_queryset(self.request.user).filter(tags=self.tags)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = self.tags
        context["title"] = self.title
        context["description"] = self.description
        return context


@superuser_required()
class TagUpdateView(UpdateView):
    """TagUpdateView UpdateView

    A view to Update a Tag

    Args:
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = CustomTag
    form = TagForm
    fields = "__all__"
    template_name = "blog/edit_tag.html"
    success_url = reverse_lazy("blog:tag_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all().order_by("-pk")[:21]
        context["title"] = "Edit Tag"
        return context


class PostCreateView(AutoPermissionRequiredMixin, CreateView):
    """PostCreateView CreateView

    A view to create a Post

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to create a Post
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    form_class = PostCreateForm
    template_name = "blog/create_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "New Post"
        return context


class CategoryCreateView(AutoPermissionRequiredMixin, CreateView):
    """CategoryCreateView

    View to Create a Category

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to create a Category
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Category
    form_class = CategoryCreateForm
    template_name = "blog/create_category.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "New Category"
        return context


class SeriesCreateView(AutoPermissionRequiredMixin, CreateView):
    """SeriesCreateView

    A view to create a Series

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to create a Series
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Series
    form_class = SeriesCreateForm
    template_name = "blog/create_series.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "New Series"
        return context


class CategoryUpdateView(AutoPermissionRequiredMixin, UpdateView):
    """CategoryUpdateView

    View to update a Category

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Category
    form_class = CategoryEditForm
    template_name = "blog/edit_category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "Edit Category"
        return context


class CategoryDeleteView(AutoPermissionRequiredMixin, UpdateView):
    """CategoryDeleteView

    A view to delete a Category

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Category
    template_name = "blog/category_confirm_delete.html"
    form_class = CategoryDeleteForm
    success_url = reverse_lazy("blog:category_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                self.category.remove()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "Delete Category"
        return context


class SeriesUpdateView(AutoPermissionRequiredMixin, UpdateView):
    """SeriesUpdateView

    A view to update a Series

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Series
    form_class = SeriesEditForm
    template_name = "blog/edit_series.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "Edit Series"
        return context


class SeriesDeleteView(AutoPermissionRequiredMixin, UpdateView):
    """SeriesDeleteView

    View to delete a Series

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Series
    template_name = "blog/series_confirm_delete.html"
    form_class = SeriesDeleteForm
    success_url = reverse_lazy("blog:series_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.series = get_object_or_404(Series, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                self.series.remove()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "Delete Series"
        return context


class PostUpdateView(AutoPermissionRequiredMixin, UpdateView):
    """PostUpdateView

    View to update a Post

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    form_class = PostEditForm
    template_name = "blog/edit_post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "Edit Post"
        return context


class PostCloneView(AutoPermissionRequiredMixin, CreateView):
    """PostCloneView Create View

    A view to clone a Post

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        CreateView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = "blog/clone_post.html"
    form_class = PostCloneForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        post = self.get_object()

        context = super().get_context_data(**kwargs)
        context["title"] = "Clone Post"
        context["form"] = PostCloneForm(instance=post)
        return context


class PostDeleteView(AutoPermissionRequiredMixin, UpdateView):
    """PostDeleteView

    View to delete a Post

    Args:
        AutoPermissionRequiredMixin ([type]): Tests if the User has the permission to do that
        UpdateView ([type]): [description]

    Raises:
        PermissionDenied: [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = "blog/post_confirm_delete.html"
    form_class = PostDeleteForm
    success_url = reverse_lazy("blog:post_list")

    def get_queryset(self):
        if self.request.user.is_superuser:
            self.removing_post = get_object_or_404(Post, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                self.removing_post.remove()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.model.objects.get_without_removed().order_by("-pk")
        context["title"] = "Delete Post"
        return context


@user_passes_test(lambda u: u.is_superuser)
def post_publish(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect("blog:post_detail", slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def post_publish_withdrawn(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.withdrawn = True
    post.publish_withdrawn()
    return redirect("blog:post_detail", slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def post_needs_review(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.needs_review()
    return redirect("blog:post_detail", slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def category_needs_review(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.needs_review()
    return redirect("blog:post_category_list", slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def series_needs_review(request, slug):
    series = get_object_or_404(Series, slug=slug)
    series.needs_review()
    return redirect("blog:post_series_list", slug=slug)


class PostDayArchiveView(DayArchiveView):
    """PostDayArchiveView

    Archive by day

    Args:
        DayArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    model = Post
    template_name = "blog/lists/post_list.html"
    context_object_name = "posts"
    paginate_by = 20
    paginate_orphans = 5
    date_field = "pub_date"
    allow_future = True

    def get_queryset(self):
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = (
            "[Archive] Posted the " + str(self.get_day()) + " " + str(self.get_month()) + " " + str(self.get_year())
        )
        context["archive"] = True
        context["g_day"] = f"{self.get_day()}"
        context["g_month"] = f"{self.get_month()}"
        context["g_year"] = f"{self.get_year()}"
        return context


def link_fetching(request):
    """Link Fetching for EditorJS"""
    import requests
    from bs4 import BeautifulSoup

    url = request.GET["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    metas = soup.find_all("meta")
    title = ""
    description = ""
    image = ""
    for meta in metas:
        if "property" in meta.attrs:
            if meta.attrs["property"] == "og:image":
                image = meta.attrs["content"]
        elif "name" in meta.attrs:
            if meta.attrs["name"] == "description":
                description = meta.attrs["content"]
            if meta.attrs["name"] == "title":
                title = meta.attrs["content"]

    return JsonResponse(
        {
            "success": 1,
            "meta": {
                "description": description,
                "title": title,
                "image": {"url": image},
            },
        }
    )
