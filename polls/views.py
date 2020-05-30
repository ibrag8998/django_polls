from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'most_recent'

    def get_queryset(self):
        """ Return the most recent 5 questions """
        return Question.objects.filter(
            pub_date__lte=timezone.now(),
            choice__text__isnull=False).distinct().order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    template_name = 'polls/detail.html'
    context_object_name = 'q'

    def get_queryset(self):
        """ Filter questions.
        Filter: exclude not yet published questions.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    context_object_name = 'q'


def vote(req, q_id):
    q = get_object_or_404(Question, pk=q_id)
    try:
        selected_choice = q.choice_set.get(pk=req.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        messages.add_message(req, messages.INFO, "You didn't select a choice")
        return redirect('polls:detail', q.id)

    selected_choice.votes += 1
    selected_choice.save()
    return redirect('polls:results', q.id)
    return HttpResponseRedirect(reverse('polls:results', args=(q.id, )))
