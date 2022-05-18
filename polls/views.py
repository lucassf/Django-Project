from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at 5c2175a3 the polls index.")
