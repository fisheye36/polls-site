from django.http import Http404, HttpResponse
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-publication_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question with ID=%d does not exist' % question_id)
    context = {'question': question}
    return render(request, 'polls/detail.html', context)


def results(request, question_id):
    return HttpResponse(b"You're looking at the results of question '%d'" % question_id)


def vote(request, question_id):
    return HttpResponse(b"You're voting on question '%d'" % question_id)
