from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.filter(publication_date__lte=timezone.now()).order_by('-publication_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    model = Question

    def get_queryset(self):
        return Question.objects.filter(publication_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    template_name = 'polls/results.html'
    model = Question


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    def render_with_error(error_message):
        return render(request, 'polls/detail.html', context={
            'question': question,
            'error_message': error_message,
        })

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except KeyError:
        return render_with_error("You didn't select a choice.")
    except Choice.DoesNotExist:
        return render_with_error("There is no such choice for this question.")
    selected_choice.votes = F('votes') + 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
