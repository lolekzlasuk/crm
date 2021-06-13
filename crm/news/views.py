from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .forms import NewsForm, NewsFileForm, DocumentFForm, DocQuestionForm, UserQuestionForm, DocFileForm
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import News, NewsFile, Notification, NotificationReadFlag, NewsReadFlag, DocumentF, DocFile, DocQuestion, KnowledgeCategory, UserQuestion
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
import json


class KnowledgeCategoryListView(ListView):
    model = KnowledgeCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        files = DocFile.objects.filter(
            Q(target_location=self.request.user.userprofile.location) | Q(
            target_location="ALL"))

        context['files'] = files.filter(Q
            (target_departament=self.request.user.userprofile.departament) | Q(
            target_departament="ALL")).order_by('-date_created')[:10]

        documents = DocumentF.objects.filter(
            Q(target_location=self.request.user.userprofile.location) | Q(
            target_location="ALL"))

        context['docs'] = documents.filter(Q
            (target_departament=self.request.user.userprofile.departament) | Q(
            target_departament="ALL")).order_by('-date_created')[:10]

        return context


class KnowledgeCategoryDetailView(DetailView):
    model = KnowledgeCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        files = self.object.files

        files = files.filter(
            Q(target_location=self.request.user.userprofile.location) | Q(
                target_location="ALL"))

        context['files'] = files.filter(Q
            (target_departament=self.request.user.userprofile.departament) | Q(
            target_departament="ALL")).order_by('-date_created')

        documents = self.object.docs.filter(
            Q(target_location=self.request.user.userprofile.location) | Q(
            target_location="ALL"))

        context['docs'] = documents.filter(Q
            (target_departament=self.request.user.userprofile.departament) | Q(
            target_departament="ALL")).order_by('-date_created')

        context['categories'] = KnowledgeCategory.objects.all()

        return context


class QuestionListView(ListView):
    model = DocQuestion

    def get_queryset(self):
        userprofile = self.request.user.userprofile
        qs = DocQuestion.objects.exclude(answer=None)

        qs = qs.filter(Q(target_location=userprofile.location) | Q(
            target_location="ALL"))

        qs = qs.filter(Q(target_departament=userprofile.departament) | Q(
            target_departament="ALL")).order_by('-date_created')

        if self.request.GET.get('category') != None:
            query = self.request.GET.get('category')
            qs = qs.filter(Q(category=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = KnowledgeCategory.objects.all()
        return context


class UnansweredQuestionListView(ListView):
    model = UserQuestion
    template_name = "news/answer.html"


class QuestionUpdateView(UpdateView):
    model = DocQuestion
    form_class = DocQuestionForm
    success_url = '/QandA/'

    template_name = "news/upload.html"


class UnpublishedNewsListView(LoginRequiredMixin,
                                PermissionRequiredMixin, ListView):
    model = News
    permission_required = ('news.can_edit',)

    def get_queryset(self):
        return News.objects.filter(published_date=None).exclude(
            staticdoc=True).order_by('-date_created')


class NewsDetailView(LoginRequiredMixin, DetailView):
    model = News


class DocDetailView(LoginRequiredMixin, DetailView):
    model = DocumentF


class NewsListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['activate'] = NewsReadFlag.objects.filter(
            user=self.request.user, read=False).values_list('news', flat=True)
        return context

    def get_queryset(self):
        userprofile = self.request.user.userprofile
        qs = News.objects.exclude(published_date=None).exclude(
            staticdoc=True).order_by('-published_date')
        qs = qs.filter(Q(target_location=userprofile.location) | Q(
            target_location="ALL"))
        qs = qs.filter(Q(target_departament=userprofile.departament) | Q(
            target_departament="ALL"))
        return qs


@login_required
def post_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        file_form = NewsFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        if form.is_valid() and file_form.is_valid():
            news_instance = form.save(commit=False)
            news_instance.author = User.objects.get(
                username=request.user.username)
            news_instance.save()
            for f in files:
                file_instance = NewsFile.objects.save_file(f)
                file_instance.save()
                news_instance.files.add(file_instance.id)
            return redirect('news:unpublished')
    else:
        form = NewsForm()
        file_form = NewsFileForm()

    return render(request, 'news/upload.html',
        {'form': form, 'file_form': file_form})


def answer_question(request, pk):
    question = get_object_or_404(UserQuestion, pk=pk)
    if request.method == 'POST':
        form = DocQuestionForm(request.POST)
        if form.is_valid():
            form.save()
            UserQuestion.objects.get(pk=pk).delete()
    else:
        data = {'title': question.title, 'body': question.body}
        form = DocQuestionForm(initial=data)

    return render(request, 'news/upload.html', {'form': form})


@login_required
def publish_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.publish()
    return redirect('news:newss')


@login_required
def flagtoggle(request):

    if request.is_ajax() and request.method == 'POST':
        pk = json.loads(request.body).get('pk')
        user = User.objects.get(username=request.user)
        news = News.objects.get(pk=pk)
        notification = Notification.objects.get(news=news)
        notificationreadflag = NotificationReadFlag.objects.get(
            user=user, notification=notification)
        notificationreadflag.read = True
        notificationreadflag.save()
        newsreadflag = NewsReadFlag.objects.get(user=user, news=news)
        newsreadflag.read = True
        newsreadflag.save()
        return HttpResponse("OK")


@login_required
def newsreadflagtoggle(request):

    if request.is_ajax() and request.method == 'POST':
        pk = json.loads(request.body).get('pk')
        user = User.objects.get(username=request.user.username)
        newsreadflag = NewsReadFlag.objects.get(
            user=user, news=News.objects.get(pk=pk))
        newsreadflag.read = True
        newsreadflag.save()
        return HttpResponse("OK")


@login_required
def markall(request):

    if request.is_ajax() and request.method == 'POST':
        user = User.objects.get(username=request.user)
        notificationreadflag = NotificationReadFlag.objects.filter(user=user)
        for each in notificationreadflag:

            each.read = True
            each.save()
        newsreadflag = NewsReadFlag.objects.filter(user=user)
        for each in newsreadflag:
            each.read = True
            each.save()
        return HttpResponse("OK")


@login_required
def post_document(request):
    if request.method == 'POST':
        form = DocumentFForm(request.POST)

        if form.is_valid():
            news_instance = form.save(commit=False)
            news_instance.author = User.objects.get(
                username=request.user.username)
            news_instance.save()
            return redirect('news:newss')
    else:
        form = DocumentFForm()
    return render(request, 'news/upload.html', {'form': form})


@login_required
def post_file(request):
    if request.method == 'POST':
        form = DocFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        for f in files:
            file_instance = form.save(commit=False)
            file_instance.isnews = False
            file_instance.save()
            return redirect('news:files')
    else:
        form = DocFileForm()
    return render(request, 'news/upload.html', {'form': form})


@login_required
def post_question(request):
    if request.method == 'POST':
        form = DocQuestionForm(request.POST)

        if form.is_valid():
            news_instance = form.save(commit=False)
            news_instance.save()
            return redirect('news:QandA')
    else:
        form = DocQuestionForm()
    return render(request, 'news/upload.html', {'form': form})


@login_required
def post_userquestion(request):
    if request.method == 'POST':
        form = UserQuestionForm(request.POST)

        if form.is_valid():
            news_instance = form.save(commit=False)
            news_instance.author = User.objects.get(
                username=request.user.username)
            news_instance.save()
            return redirect('news:QandA')
    else:
        form = UserQuestionForm()
    return render(request, 'news/upload.html', {'form': form})
