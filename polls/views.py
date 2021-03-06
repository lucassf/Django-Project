from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db.models import F

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'lastest_questions'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]


def owner(request):
    return HttpResponse("Hello, world. 0801f1b5 is the polls owner.")


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


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
