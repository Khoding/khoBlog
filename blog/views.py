from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.views.generic.dates import (
    ArchiveIndexView,
    DayArchiveView,
    MonthArchiveView,
    WeekArchiveView,
    YearArchiveView,
)

from rules.contrib.views import AutoPermissionRequiredMixin

from blog.filters import PostFilter
from custom_taggit.models import CustomTag
from khoBlog import settings
from khoBlog.utils.superuser_required import superuser_required, superuser_required_ignore_secure_mode

from .forms import (
    CategoryCreateForm,
    CategoryDeleteForm,
    CategoryEditForm,
    PostCloneForm,
    PostCreateForm,
    PostDefineFeaturedCategoryForm,
    PostDeleteForm,
    PostEditForm,
    PostMarkOutdatedForm,
    SeriesCreateForm,
    SeriesDeleteForm,
    SeriesEditForm,
)
from .mixins import CategoryListMixin, PostListMixin, SeriesListMixin
from .models import Category, Post, PostCatsLink, Series


class PostListView(PostListMixin, ListView):
    """PostListView List View

    The default List View for Posts

    Args:
        ListView (ListView): Lists elements

    Returns:
        posts: A list of posts
    """

    def get_queryset(self):
        """Get queryset"""
        query = PostFilter(
            self.request.GET,
            queryset=Post.objects.filter(Q(pub_date__lte=timezone.now(), withdrawn=False)),
        )
        if "page" not in query.data and query.data != {} or "title" in query.data and "page" in query.data:
            return query.qs
        if settings.HIDE_WEDNESDAY:
            return Post.objects.get_base_common_queryset().get_without_wednesday()
        return Post.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Latest Posts"
        context["filter_form"] = PostFilter()
        context["has_rss"] = True
        return context


class AllPostListView(PostListMixin, ListView):
    """AllPostListView List View

    The List View for Posts that shows all posts

    Args:
        ListView (ListView): Lists elements

    Returns:
        posts: A list of posts
    """

    def get_queryset(self):
        """Get queryset"""
        if self.request.user.is_superuser and self.request.user.secure_mode is True:
            raise PermissionDenied
        query = PostFilter(
            self.request.GET,
            queryset=Post.objects.get_without_removed(),
        )
        if query is not None and query != "":
            return query.qs
        return Post.objects.get_base_common_queryset()

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Latest Posts"
        context["filter_form"] = PostFilter()
        return context


class PostInCategoryListView(PostListMixin, ListView):
    """PostInCategoryListView List View

    Lists all Posts in a particular Category

    Args:
        ListView (ListView): A list View

    Raises:
        PermissionDenied: If the currently logged in user doesn't have access to the requested Category

    Returns:
        posts: A list of posts
    """

    def get_queryset(self):
        """Get queryset"""
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        if not self.category.withdrawn or self.request.user.is_superuser and self.request.user.secure_mode is False:
            self.title = self.category.full_title
            self.description = self.category.description
        else:
            raise PermissionDenied
        return self.model.objects.get_common_queryset(self.request.user).filter(categories=self.category)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["parent_object"] = self.category
        context["title"] = self.title
        context["description"] = self.description
        context["has_rss"] = True
        return context


class PostInSeriesListView(PostListMixin, ListView):
    """PostInSeriesListView List View

    Lists all Posts in a particular Series

    Args:
        ListView (ListView): A list View

    Raises:
        PermissionDenied: If the currently logged in user doesn't have access to the requested Series

    Returns:
        posts: A list of posts
    """

    def get_queryset(self):
        """Get queryset"""
        self.series = get_object_or_404(Series, slug=self.kwargs["slug"])
        if not self.series.withdrawn or self.request.user.is_superuser and self.request.user.secure_mode is False:
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
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["parent_object"] = self.series
        context["title"] = self.series.title
        context["description"] = self.description
        return context


def redirect_to_first_in_category(request, slug):
    """redirects to the first post in category"""
    category = get_object_or_404(Category, slug=slug)
    if request.user.is_superuser and request.user.secure_mode is False:
        first = Post.objects.filter(categories=category).order_by("pk").first()
    else:
        first = (
            Post.objects.filter(categories=category)
            .filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None)
            .order_by("pk")
            .first()
        )
    return redirect(reverse("blog:post_detail", args=(first.slug,)))


def redirect_to_latest_in_category(request, slug):
    """redirects to the latest post in category"""
    category = get_object_or_404(Category, slug=slug)
    if request.user.is_superuser and request.user.secure_mode is False:
        latest = Post.objects.filter(categories=category).latest()
    else:
        latest = (
            Post.objects.filter(categories=category)
            .filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None)
            .latest()
        )
    return redirect(reverse("blog:post_detail", args=(latest.slug,)))


def redirect_to_first_in_series(request, slug):
    """redirects to the first post in series"""
    series = get_object_or_404(Series, slug=slug)
    if request.user.is_superuser and request.user.secure_mode is False:
        first = Post.objects.filter(series=series).order_by("pk").first()
    else:
        first = (
            Post.objects.filter(series=series)
            .filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None)
            .order_by("pk")
            .first()
        )
    return redirect(reverse("blog:post_detail", args=(first.slug,)))


def redirect_to_latest_in_series(request, slug):
    """redirects to the latest post in series"""
    series = get_object_or_404(Series, slug=slug)
    if request.user.is_superuser and request.user.secure_mode is False:
        latest = Post.objects.filter(series=series).latest()
    else:
        latest = (
            Post.objects.filter(series=series)
            .filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None)
            .latest()
        )
    return redirect(reverse("blog:post_detail", args=(latest.slug,)))


class CategoryListView(CategoryListMixin, ListView):
    """CategoryListView ListView

    A list of Categories

    Args:
        ListView ([type]): [description]

    Returns:
        category_list: A list of Categories
    """

    ordering = "pk"

    def get_queryset(self):
        """Get the queryset for this view."""
        if self.request.user.is_superuser and self.request.user.secure_mode is False:
            return self.model.objects.get_without_removed()
        return self.model.objects.filter(withdrawn=False).get_without_removed()

    def get_context_data(self, **kwargs):
        """Gets the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Category List"
        context["description"] = "List of categories"
        return context


class SeriesListView(SeriesListMixin, ListView):
    """SeriesListView ListView

    A list of Series

    Args:
        ListView ([type]): [description]

    Returns:
        series_list: A list of Series
    """

    def get_queryset(self):
        """Get the queryset for this view."""
        if self.request.user.is_superuser and self.request.user.secure_mode is False:
            return self.model.objects.get_without_removed()
        return self.model.objects.filter(withdrawn=False).get_without_removed()

    def get_context_data(self, **kwargs):
        """Gets the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Series List"
        context["description"] = "List of series"
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
        """Get the queryset for this view."""
        self.post = get_object_or_404(Post, slug=self.kwargs["slug"])
        self.post.clicked()
        if self.post.deleted_at:
            raise Http404
        if self.request.user.is_superuser and self.request.user.secure_mode is False:
            self.series = (
                self.model.objects.get_queryset()
                .filter(series__isnull=False, series=self.post.series)
                .order_by("order_in_series")
            )
            self.title = self.post.title
            self.description = self.post.description
            if self.post.pub_date:
                self.prev_post = (
                    Post.objects.filter(pub_date__lt=self.post.pub_date, deleted_at=None)
                    .exclude(pk=self.post.pk)
                    .order_by("-pub_date")
                    .first()
                )
                self.next_post = (
                    Post.objects.filter(pub_date__gt=self.post.pub_date, deleted_at=None)
                    .exclude(pk=self.post.pk)
                    .order_by("pub_date")
                    .first()
                )
            else:
                self.prev_post = (
                    Post.objects.filter(created_date__lt=self.post.created_date, deleted_at=None)
                    .exclude(pk=self.post.pk)
                    .order_by("-created_date")
                    .first()
                )
                self.next_post = (
                    Post.objects.filter(created_date__gt=self.post.created_date, deleted_at=None)
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
                    deleted_at=None,
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
                    deleted_at=None,
                )
                .exclude(pk=self.post.pk)
                .order_by("pub_date")
                .first()
            )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """Gets the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["series"] = self.series
        context["title"] = self.title
        context["description"] = self.description
        context["similar_posts"] = self.post.tags.similar_objects()[:3]
        context["next_post"] = self.next_post
        context["prev_post"] = self.prev_post
        return context


def post_like(request, slug):
    """View to like a post"""
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        post.likes.add(request.user)
        messages.add_message(request, messages.SUCCESS, f"You liked {post.title}")
    else:
        messages.add_message(request, messages.WARNING, "You must be logged in to like a post")
    return HttpResponseRedirect(reverse("blog:post_detail", kwargs={"slug": slug}))


def post_dislike(request, slug):
    """View to dislike a post"""
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_authenticated:
        post.likes.remove(request.user)
        messages.add_message(request, messages.SUCCESS, f"Your like was removed from {post.title}")
    else:
        messages.add_message(request, messages.WARNING, "You must be logged in to dislike a post")
    return HttpResponseRedirect(reverse("blog:post_detail", kwargs={"slug": slug}))


def redirect_to_latest(request):
    """redirects to the latest post"""
    if request.user.is_superuser and request.user.secure_mode is False:
        latest = Post.objects.latest()
    else:
        latest = Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None).latest()
    return redirect(reverse("blog:post_detail", args=(latest.slug,)))


def redirect_to_random(request):
    """redirects to a random post"""
    if request.user.is_superuser and request.user.secure_mode is False:
        post = Post.objects.filter(deleted_at=None).order_by("?")[0]
    else:
        post = Post.objects.filter(pub_date__lte=timezone.now(), withdrawn=False, deleted_at=None).order_by("?")[0]
    post.rnd_chosen()
    messages.add_message(
        request,
        messages.SUCCESS,
        f"You were redirected to {post.title}",
    )
    return redirect(reverse("blog:post_detail", args=(post.slug,)))


def post_detail_through_id(request, pk):
    """redirects to a post by id"""
    post = get_object_or_404(Post, pk=pk)
    return redirect(reverse("blog:post_detail", args=(post.slug,)))


@superuser_required_ignore_secure_mode()
class PostDraftListView(PostListMixin, ListView):
    """PostDraftListView ListView

    Lists Draft Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    def get_queryset(self):
        """get_queryset"""
        return self.model.objects.filter(pub_date__isnull=True).order_by("-created_date").get_without_removed()

    def get_context_data(self, **kwargs):
        """Gets the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Drafts"
        context["description"] = "List of draft posts"
        return context


@superuser_required_ignore_secure_mode()
class PostScheduledListView(PostListMixin, ListView):
    """PostScheduledListView ListView

    Lists Scheduled Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    def get_queryset(self):
        """get_queryset"""
        return (
            self.model.objects.filter(pub_date__gte=timezone.now(), withdrawn=False)
            .get_without_removed()
            .order_by("pub_date")
        )

    def get_context_data(self, **kwargs):
        """Gets the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Scheduled"
        context["description"] = "List of scheduled posts"
        return context


# superuser is required to access this view because it can contain secured content
@superuser_required()
class PostWithdrawnListView(PostListMixin, ListView):
    """PostWithdrawnListView ListView

    Lists Withdrawn Posts

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    def get_queryset(self):
        """get_queryset"""
        return self.model.objects.filter(withdrawn=True).get_without_removed()

    def get_context_data(self, **kwargs):
        """Gets the context data for the view."""
        context = super().get_context_data(**kwargs)
        context["title"] = "Withdrawn"
        context["description"] = "List of withdrawn posts"
        return context


class PostWithTagListView(PostListMixin, ListView):
    """PostWithTagListView ListView

    Lists all Posts tagged with a given Tag

    Args:
        ListView ([type]): [description]

    Returns:
        posts: A list of posts
    """

    def get_queryset(self):
        """get_queryset"""
        self.tags = get_object_or_404(CustomTag, slug=self.kwargs["slug"])
        self.title = f"Tag: {self.tags.name}"
        self.description = f"Posts tagged with {self.tags.name}"
        return self.model.objects.get_common_queryset(self.request.user).filter(tags=self.tags)

    def get_context_data(self, **kwargs):
        """Get context data for the view."""
        context = super().get_context_data(**kwargs)
        context["parent_object"] = self.tags
        context["title"] = self.title
        context["description"] = self.description
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
        """form_valid"""
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS, f"{form.instance.title} was created successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "New Post"
        return context


class PostDefineFeaturedCategoryUpdateView(UpdateView):
    """PostDefineFeaturedCategoryUpdateView UpdateView

    A view to set the featured category of a post
    """

    model = Post
    form_class = PostDefineFeaturedCategoryForm
    template_name = "blog/post_define_featured_category.html"

    def get_form_kwargs(self):
        """Passes the request object to the form class.
        This allows to get the queryset for the featured_cat field.
        """
        kwargs = super(PostDefineFeaturedCategoryUpdateView, self).get_form_kwargs()
        kwargs["post"] = self.get_object()
        return kwargs

    def form_valid(self, form):
        """form_valid"""
        # There's probably a better way to do this, but it seems that Django doesn't handle through fields really well
        # And since this is a once a week action, I'd rather have this than having to go to the Admin to set it
        postcat = form.instance.postcatslink_set.all()  # get all the postcatslinks for the post
        for link in postcat:  # for each postcatslink
            link.featured_cat = False  # set the featured_cat to False
            link.save()  # save the changes
        postcatslink = PostCatsLink.objects.get(
            post=self.get_object(), category=form.cleaned_data["featured_cat"]
        )  # get the postcatslink with the chosen featured_cat
        postcatslink.featured_cat = True  # set the featured_cat to True
        postcatslink.save()  # save the changes
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f"{form.instance.title}'s featured category was set to {postcatslink.category}",
        )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Get context data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Define the post's featured category"
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
        """form_valid"""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Get context data for the view."""
        context = super().get_context_data(**kwargs)
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
        """get_context_data"""
        context = super().get_context_data(**kwargs)
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
        """get_context_data"""
        context = super().get_context_data(**kwargs)
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
        """get_queryset"""
        if self.request.user.is_superuser:
            self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                self.category.soft_delete()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
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
        """get_context_data"""
        context = super().get_context_data(**kwargs)
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
        """get_queryset"""
        if self.request.user.is_superuser:
            self.series = get_object_or_404(Series, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                self.series.soft_delete()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
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

    def form_valid(self, form):
        """form_valid"""
        messages.add_message(self.request, messages.SUCCESS, f"{form.instance.title} was edited successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
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
        """form_valid"""
        form.instance.author = self.request.user
        messages.add_message(self.request, messages.SUCCESS, f"{form.instance.title} was cloned successfully")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """get_context_data"""
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
        """Get the queryset for this view."""
        if self.request.user.is_superuser:
            removing_post = get_object_or_404(Post, slug=self.kwargs["slug"])
            if self.get_form().is_valid():
                removing_post.soft_delete()
        else:
            raise PermissionDenied()
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Delete Post"
        return context


def post_next(request, slug):
    """post_next"""
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_superuser and request.user.secure_mode is False:
        if post.pub_date:
            next_post = (
                Post.objects.filter(pub_date__gt=post.pub_date, deleted_at=None)
                .exclude(pk=post.pk)
                .order_by("pub_date")
                .first()
            )
        else:
            next_post = (
                Post.objects.filter(created_date__gt=post.created_date, deleted_at=None)
                .exclude(pk=post.pk)
                .order_by("created_date")
            )
    else:
        next_post = (
            Post.objects.filter(
                pub_date__gt=post.pub_date,
                pub_date__lte=timezone.now(),
                withdrawn=False,
                deleted_at=None,
            )
            .exclude(pk=post.pk)
            .order_by("pub_date")
            .first()
        )
    if next_post is not None:
        next_post = next_post.get_absolute_url()
    else:
        next_post = post.get_absolute_url()
    return HttpResponseRedirect(next_post)


def post_previous(request, slug):
    """post_previous"""
    post = get_object_or_404(Post, slug=slug)
    if request.user.is_superuser and request.user.secure_mode is False:
        if post.pub_date:
            prev_post = (
                Post.objects.filter(pub_date__lt=post.pub_date, deleted_at=None)
                .exclude(pk=post.pk)
                .order_by("-pub_date")
                .first()
            )
        else:
            prev_post = (
                Post.objects.filter(created_date__lt=post.created_date, deleted_at=None)
                .exclude(pk=post.pk)
                .order_by("-created_date")
                .first()
            )
    else:
        prev_post = (
            Post.objects.filter(
                pub_date__lt=post.pub_date,
                pub_date__lte=timezone.now(),
                withdrawn=False,
                deleted_at=None,
            )
            .exclude(pk=post.pk)
            .order_by("-pub_date")
            .first()
        )
    if prev_post is not None:
        prev_post = prev_post.get_absolute_url()
    else:
        prev_post = post.get_absolute_url()
    return HttpResponseRedirect(prev_post)


@user_passes_test(lambda u: u.is_superuser)
def post_publish(request, slug):
    """publishes a post"""
    post = get_object_or_404(Post, slug=slug)
    post.publish()
    return redirect("blog:post_detail", slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def post_publish_withdrawn(request, slug):
    """publishes a post as withdrawn"""
    post = get_object_or_404(Post, slug=slug)
    post.withdrawn = True
    post.publish_withdrawn()
    return redirect("blog:post_detail", slug=slug)


@superuser_required_ignore_secure_mode()
class PostIsOutdatedUpdateView(UpdateView):
    """PostIsOutdatedUpdateView

    View to mark a post as outdated
    """

    model = Post
    template_name = "blog/post_confirm_outdated.html"
    form_class = PostMarkOutdatedForm

    def form_valid(self, form):
        """what happens when the form is valid"""
        post = self.get_object()
        if form.instance.is_content_outdated_date:
            form.instance.is_content_outdated_date = form.instance.is_content_outdated_date
        elif post.is_content_outdated_date is not None and form.instance.is_content_outdated_date is None:
            form.instance.is_content_outdated_date = None
        else:
            form.instance.is_content_outdated_date = timezone.now()
        form.instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "Mark post as outdated"
        return context


@user_passes_test(lambda u: u.is_superuser)
def post_needs_review(request, slug):
    """marks a post as needing review"""
    post = get_object_or_404(Post, slug=slug)
    post.needs_review()
    return redirect("blog:post_detail", slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def category_needs_review(request, slug):
    """marks a category as needing review"""
    category = get_object_or_404(Category, slug=slug)
    category.needs_review()
    return redirect("blog:post_category_list", slug=slug)


@user_passes_test(lambda u: u.is_superuser)
def series_needs_review(request, slug):
    """marks a series as needing review"""
    series = get_object_or_404(Series, slug=slug)
    series.needs_review()
    return redirect("blog:post_series_list", slug=slug)


class PostArchiveIndexView(PostListMixin, ArchiveIndexView):
    """PostArchiveIndexView

    Archive view

    Args:
        ArchiveIndexView ([type]): [description]

    Returns:
        [type]: [description]
    """

    make_object_list = True
    date_field = "pub_date"
    allow_future = True

    def get_queryset(self):
        """get_queryset"""
        return self.model.objects.get_common_queryset(self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "[Archive] Post archive"
        context["archive"] = True
        return context


class PostYearArchiveView(PostListMixin, YearArchiveView):
    """PostYearArchiveView

    Archive by year

    Args:
        YearArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    make_object_list = True
    date_field = "pub_date"
    allow_future = True

    def get_queryset(self):
        """get_queryset"""
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "[Archive] Posted in " + str(self.get_year())
        context["archive"] = True
        return context


class PostMonthArchiveView(PostListMixin, MonthArchiveView):
    """PostMonthArchiveView

    Archive by month

    Args:
        MonthArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    date_field = "pub_date"
    allow_future = True

    def get_queryset(self):
        """get_queryset"""
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "[Archive] Posted in " + str(self.get_month()) + " of " + str(self.get_year())
        context["archive"] = True
        return context


class PostWeekArchiveView(PostListMixin, WeekArchiveView):
    """PostWeekArchiveView

    Archive by week

    Args:
        WeekArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    date_field = "pub_date"
    week_format = "%W"
    allow_future = True

    def get_queryset(self):
        """get_queryset"""
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        """get_context_data"""
        context = super().get_context_data(**kwargs)
        context["title"] = "[Archive] Posted during Week " + str(self.get_week()) + " of " + str(self.get_year())
        context["archive"] = True
        return context


class PostDayArchiveView(PostListMixin, DayArchiveView):
    """PostDayArchiveView

    Archive by day

    Args:
        DayArchiveView ([type]): [description]

    Returns:
        [type]: [description]
    """

    date_field = "pub_date"
    allow_future = True

    def get_queryset(self):
        """Get the queryset for this view."""
        return self.model.objects.get_common_queryset(user=self.request.user).get_without_removed()

    def get_context_data(self, **kwargs):
        """Get the context data for this view."""
        context = super().get_context_data(**kwargs)
        context["title"] = (
            "[Archive] Posted the " + str(self.get_day()) + " " + str(self.get_month()) + " " + str(self.get_year())
        )
        context["archive"] = True
        context["g_day"] = f"{self.get_day()}"
        context["g_month"] = f"{self.get_month()}"
        context["g_year"] = f"{self.get_year()}"
        return context


def redirect_post(request, vanity_url):
    """redirect_post

    Redirects from vanity urls to the actual post
    """
    post = get_object_or_404(Post, vanity_url=vanity_url)
    return redirect(post.get_absolute_url())
