from django.http import HttpResponse


def index(request):
    return HttpResponse(b'Hello world, you are at the polls app index page.')
