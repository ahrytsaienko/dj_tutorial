from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.views import generic
from django.utils import timezone


class IndexView(generic.ListView):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        :return: last 5 question except future qiestions
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, 'polls/detail.html', {'question': question})

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choise = question.choice_set.get(pk=request.POST['choice'])
    except:
        (KeyError, Choice.DoesNotExist)
        return render(request, 'polls/detail.html', {'question': question,
                                                     'eror_message': "You didn't select a choice."
                                                     })
    else:
        selected_choise.votes += 1
        selected_choise.save()
        return HttpResponseRedirect(
            reverse('polls:results', args=(question_id,)))
