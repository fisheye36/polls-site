from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Choice, Question


def index(request):
    latest_question_list = Question.objects.order_by('-publication_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    return HttpResponse(b"You're looking at the results of question '%d'" % question_id)


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
    selected_choice.votes += 1
    selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id, )))
