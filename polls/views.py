from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from rules.contrib.views import permission_required

from .models import Choice, Question


class IndexView(PermissionRequiredMixin, ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    permission_required = "polls.view_question"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Polls List"
        context["description"] = "Polls List"
        context["app_title"] = "Polls"
        context["app_direct_link"] = reverse_lazy("polls:index")
        return context


class PollsDetailView(PermissionRequiredMixin, DetailView):
    model = Question
    template_name = "polls/detail.html"
    permission_required = "polls.view_question"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Poll Detail"
        context["description"] = "Polls Details"
        context["app_title"] = "Polls"
        context["app_direct_link"] = reverse_lazy("polls:index")
        return context


class ResultsView(PermissionRequiredMixin, DetailView):
    model = Question
    template_name = "polls/results.html"
    permission_required = "polls.view_question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Poll Results"
        context["description"] = "Polls Results"
        context["app_title"] = "Polls"
        context["app_direct_link"] = reverse_lazy("polls:index")
        return context


@permission_required("polls.view_question")
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.related_question.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
                "title": "Poll Detail",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
