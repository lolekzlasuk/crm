
from django.shortcuts import render, get_object_or_404,redirect
from .forms import QuestionForm,AnswerForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import Question,Answer,BoardCategory
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


class Question2ListView(ListView):
    model = Question


    def get(self, request, *args, **kwargs):
        if self.username != request.user.username:
            return redirect('suggestions:questionlist')
        else:
            return render(request, self.template_name)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BoardCategory.objects.all()
        return context

class QuestionListView(ListView):
    model = Question
    paginate_by = 5
    def get_queryset(self):
        queryset = Question.objects.order_by('-last_answer')
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BoardCategory.objects.all()
        return context


class QuestionDetailView(DetailView):
    model = Question


class CategoryDetailView(ListView):
    model = BoardCategory

    template_name = 'suggestions/boardcategory_detail.html'
    def get_queryset(self,**kwargs):
        queryset = Question.objects.all().filter(
            category_id = self.kwargs['pk']).order_by('-last_answer')
        return queryset

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = BoardCategory.objects.filter(pk = self.kwargs['pk'])
        context['categories'] = BoardCategory.objects.all()
        return context

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = User.objects.get(username=request.user.username)
            instance.save()
            return redirect('suggestions:questionlist')
    else:
        form = QuestionForm()
    return render(request, 'suggestions/questionform.html', {'form': form})


@login_required
def post_answer(request,pk):
     question = get_object_or_404(Question,pk=pk)
     context = {}
     if request.method == 'POST':
         form = AnswerForm(request.POST)

         if form.is_valid():
             question.answered = True
             question.last_answer = timezone.now()
             question.save()
             instance = form.save(commit=False)
             instance.author = User.objects.get(username=request.user.username)
             instance.Question = question
             instance.save()
             return redirect('suggestions:questionlist')
     else:
         form = AnswerForm()
     return render(request, 'suggestions/answerform.html', {'form': form})
