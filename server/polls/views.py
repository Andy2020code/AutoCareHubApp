from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, Http404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView

from . models import Question, Choice

# Create your views here.

def index(request):
    latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'polls/index.html', context)







class QuestionDetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        # Exclude questions with a pub_date in the future
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.pub_date > timezone.now():
            raise Http404("Question does not exist")
        return obj
    


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})



def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])

    except (KeyError, Choice.DoesNotExist):
        # redirect to the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    
    else:
        selected_choice.votes += 1
        selected_choice.save()

        # always return an HttpResponseRedirect after successfully dealing with POST data. 
        # This prevents data from being posted twice if a user hits the back button.

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))