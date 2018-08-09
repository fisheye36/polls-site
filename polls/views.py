from django.http import HttpResponse


def index(request):
    return HttpResponse(b'Hello world, you are at the polls app index page.')


def detail(request, question_id):
    return HttpResponse(b"You're looking at question '%d'" % question_id)


def results(request, question_id):
    return HttpResponse(b"You're looking at the results of question '%d'" % question_id)


def vote(request, question_id):
    return HttpResponse(b"You're voting on question '%d'" % question_id)
