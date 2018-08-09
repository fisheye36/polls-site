from django.http import HttpResponse
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-publication_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


def detail(request, question_id):
    return HttpResponse(b"You're looking at question '%d'" % question_id)


def results(request, question_id):
    return HttpResponse(b"You're looking at the results of question '%d'" % question_id)


def vote(request, question_id):
    return HttpResponse(b"You're voting on question '%d'" % question_id)
