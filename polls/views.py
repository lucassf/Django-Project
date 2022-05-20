from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Question


def index(request):
    lastest_questions = Question.objects.order_by('-pub_date')[:5]
    context = {
        'lastest_questions': lastest_questions
    }
    return render(request, 'polls/index.html', context)


def owner(request):
    return HttpResponse("Hello, world. 5da04d67 is the polls index.")


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    return HttpResponse(f"You're looking at the results of question {question_id}.")


def vote(request, question_id):
    return HttpResponse(f"You're voting on question {question_id}.")
