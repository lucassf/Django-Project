from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F

from .models import Question, Choice


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
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice"
            })
    else:
        choice.votes = F('votes') + 1
        choice.save()
        choice.refresh_from_db()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
