
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PollForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Poll, Question, Answer, PollSubmition, PollSubmitionQuestion
from django.utils import timezone
from django.contrib import messages
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import permission_required


class PollListAnswerView(PermissionRequiredMixin,
                            LoginRequiredMixin,
                            ListView):
    model = Poll
    template_name = 'polls/poll_record_list.html'
    permission_required = 'polls.view_pollsubmition'
    def get_queryset(self):
        queryset = Poll.objects.exclude(
            published_date=None).order_by('-published_date')
        return queryset

class PollAnswerDetailView(PermissionRequiredMixin,
                            LoginRequiredMixin,
                            DetailView):
    model = Poll
    template_name = 'polls/poll_record_detail.html'
    permission_required = 'polls.view_pollsubmition'


class PollListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        # possibly add
        queryset = Poll.objects.exclude(
            published_date__lt = self.request.user.date_joined).exclude(
            published_date=None).order_by('-published_date')
        submitions_set = PollSubmition.objects.filter(
            user=self.request.user).exclude(submitions__isnull=True)
        queryset = queryset.exclude(submitions__in=submitions_set)

        return queryset


class UnpublishedPollListView(PermissionRequiredMixin,
                                LoginRequiredMixin,
                                ListView):
    permission_required = 'polls.view_pollsubmition'

    def get_queryset(self):
        return Poll.objects.filter(published_date=None).order_by('-date_created')


@login_required
@permission_required('calendary.add_poll', raise_exception=True)
def post_Poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = User.objects.get(username=request.user.username)
            instance.save()
            return redirect('polls:create_poll_question', pk=instance.pk)
    else:
        form = PollForm()
    return render(request, 'polls/pollform.html', {'form': form})


@login_required
@permission_required('calendary.edit_poll', raise_exception=True)
def publishpoll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    poll.publish()
    return redirect('polls:poll_list')


# executed for every added question
@login_required
@permission_required('polls.edit_poll', raise_exception=True)
def create_poll_question(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    context = {}
    if poll.published_date == None:
        if request.is_ajax() and request.method == 'POST':
            json_body = json.loads(request.body)
            print(json_body)
            title = json_body.get('title')
            enabletext = json_body.get('enabletext')
            type = json_body.get('type')
            answer_list = json_body.get('answers')
            order = json_body.get('order')
            instance = Question.objects.create(
                poll=poll,
                title=title,
                enabletext=enabletext,  # swapname
                type=type,
                order=order
            )
            if instance.type != "txt":
                for each in answer_list:
                    Answer.objects.create(
                        body=each,
                        question=instance
                    )
            return HttpResponse("OK")
        else:

            context = {"data": poll}
                       # "questions": Question.objects.all()}
            return render(request, 'polls/create_poll_question.html', context)
    else:
        return redirect('polls:poll_list')


# executed for every question in a poll
@login_required
def create_poll_answer(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    currentuser = request.user
    context = {}
    if request.is_ajax() and request.method == 'POST':
        submition = PollSubmition.objects.get(user=currentuser, poll=poll)
        question_pk = json.loads(request.body).get('question')
        questionobj = Question.objects.get(pk=question_pk)
        answer_list = json.loads(request.body).get('answer')
        text = json.loads(request.body).get('text')
        date = json.loads(request.body).get('date')
        if text == None and date == None:
            answerstr = str(" ")
            for counter, each in enumerate(answer_list):
                if counter > 0:
                    answerstr = answerstr + ";"
                answerstr = answerstr + str(Answer.objects.get(pk=each).body)

            answer_instance = PollSubmitionQuestion.objects.create(
                submition=submition,
                question=questionobj,
                order=questionobj.order,
                answer=answerstr,
                date=None,
                text=None,
            )
            for each in answer_list:
                answer_instance.manyanswer.add(each)
        elif text != None and len(answer_list) > 0:

            answerstr = str(" ")
            for counter, each in enumerate(answer_list):
                if counter > 0:
                    answerstr = answerstr + ";"
                answerstr = answerstr + str(Answer.objects.get(pk=each).body)
            answer_instance = PollSubmitionQuestion.objects.create(
                submition=submition,
                question=questionobj,
                answer=answerstr,
                order=questionobj.order,
                text=text,
                date=None,
            )
        elif text != None:
            answer_instance = PollSubmitionQuestion.objects.create(
                submition=submition,
                question=questionobj,
                order=questionobj.order,
                text=text,
                date=None,
            )
        elif date != None:
            answer_instance = PollSubmitionQuestion.objects.create(
                submition=submition,
                question=questionobj,
                order=questionobj.order,
                date=date,
                text=None,
            )

        # submition.date = timezone.now()
        submition.save()
        return HttpResponse("OK")
    else:
        submition, created = PollSubmition.objects.get_or_create(
            poll=poll,
            user=currentuser,
        )
        if submition.submitions.exists():

            return redirect('polls:poll_list')

        else:

            context["poll"] = Poll.objects.get(pk=pk)
            return render(request, 'polls/poll_detail.html', context)
