
from django.shortcuts import render, get_object_or_404,redirect
from .forms import PollForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Poll,Question,Answer,PollSubmition,PollSubmitionQuestion
from django.utils import timezone
from django.contrib import messages
import json
from django.middleware import csrf
from django.http import JsonResponse
import datetime



class PollListAnswerView(ListView):
    model = Poll
    template_name = 'polls/poll_record_list.html'

class PollAnswerDetailView(DetailView):
    model = Poll
    template_name = 'polls/poll_record_detail.html'




class PollListView(ListView):
    def get_queryset(self):

        polls = Poll.objects.exclude(published_date=None).exclude(published_date__lt = self.request.user.date_joined).order_by('-published_date')

        submitions_set = PollSubmition.objects.filter(user = self.request.user).exclude(submitions__isnull = True)

        polls = polls.exclude(submitions__in=submitions_set)

        return polls



class UnpublishedPollListView(ListView):
    def get_queryset(self):
        return Poll.objects.filter(published_date=None).order_by('-date_created')


# class PollDetailView(DetailView):
#     model = Poll

@login_required
def post_Poll(request):
    if request.method == 'POST':
        form = PollForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = User.objects.get(username=request.user.username)
            instance.save()
            return redirect('polls:createpoll', pk = instance.pk)
    else:
        form = PollForm()
    return render(request, 'polls/pollform.html', {'form': form})

@login_required
def publishpoll(request,pk):
    poll = get_object_or_404(Poll, pk=pk)
    poll.publish()
    return redirect('polls:polllist')


@login_required
def createpoll(request,pk):
    poll = get_object_or_404(Poll, pk=pk)
    context = {}
    if poll.published_date == None:

        if request.is_ajax() and request.method == 'POST':

            print(json.loads(request.body))
            title = json.loads(request.body).get('title')
            enabletext = json.loads(request.body).get('enabletext')
            type = json.loads(request.body).get('type')
            answers = json.loads(request.body).get('answers')
            order = json.loads(request.body).get('order')
            instance = Question.objects.create(
                poll = poll,
                title = title,
                enabletext = enabletext,
                type = type,
                order = order
                )
            if instance.type != "txt":
                for each in answers:
                    Answer.objects.create(
                    body = each,
                    question = instance
                    )
            return HttpResponse("OK")
        else:


            context = {"data": Poll.objects.get(pk=pk),
                        "questions": Question.objects.all()}
            return render(request,'polls/createpoll.html',context)
    else:
        return redirect('polls:polllist')



@login_required
def createpollAnswer(request,pk):
    poll = get_object_or_404(Poll, pk=pk)
    context = {}
    if request.is_ajax() and request.method == 'POST':
        print(json.loads(request.body))

        submition = PollSubmition.objects.get(user=User.objects.get(username=request.user.username),poll=poll)

        question = json.loads(request.body).get('question')
        questionobj = Question.objects.get(pk = question)
        answers = json.loads(request.body).get('answer')
        text = json.loads(request.body).get('text')
        date = json.loads(request.body).get('date')
        if text == None and date == None:
            answerstr = str(" ")
            for counter,each in enumerate(answers):
                if counter > 0:
                    answerstr = answerstr + ";"
                answerstr = answerstr + str(Answer.objects.get(pk=each).body)


            ans = PollSubmitionQuestion.objects.create(
            submition = submition,
            question = questionobj,
            order = questionobj.order,
            answer = answerstr,
            date = None,
            text = None,
            )
            for each in answers:
                ans.manyanswer.add(each)
        if text != None:
            ans = PollSubmitionQuestion.objects.create(
            submition = submition,
            question = questionobj,
            order = questionobj.order,
            text = text,
            date = None,
            )
        if date != None:
            ans = PollSubmitionQuestion.objects.create(
            submition = submition,
            question = questionobj,
            order = questionobj.order,
            date = date,
            text = None,
            )

        print(ans)
        print(ans.order)
        print(ans.text)
        print(ans.date)
        print(ans.manyanswer)
        print(ans.answer)
        submition.date = timezone.now()
        submition.save()
        return HttpResponse("OK")
    else:
        submition, created = PollSubmition.objects.get_or_create(
            poll = poll,
            user = User.objects.get(username=request.user.username),
            )
        if submition.submitions.exists():

            return redirect('polls:polllist')

        else:

            context["poll"] = Poll.objects.get(pk=pk)
            return render(request,'polls/poll_detail.html',context)
