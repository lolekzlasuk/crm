
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import  ListView, DetailView
from .models import *
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
import json
from django.core.exceptions import PermissionDenied



def locationdepartamentfilter(qs,userprofile):
    qs = qs.filter(Q(target_location=userprofile.location) | Q(target_location="non") & Q(target_departament=userprofile.departament) | Q(target_departament="non"))
    return qs


class KnowledgeCategoryListView(LoginRequiredMixin, ListView):
    model = KnowledgeCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.userprofile
        context['files'] = locationdepartamentfilter(DocFile.objects,user)
        context['docs'] = locationdepartamentfilter(DocumentF.objects,user)
        return context


class KnowledgeCategoryDetailView(LoginRequiredMixin, DetailView):
    model = KnowledgeCategory

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.userprofile
        context['files'] = locationdepartamentfilter(self.object.files.all(),user)
        context['docs'] = locationdepartamentfilter(self.object.docs.all(),user)
        context['categories'] = KnowledgeCategory.objects.all()
        return context


class QuestionListView(LoginRequiredMixin, ListView):
    model = DocQuestion

    def get_queryset(self):
        user = self.request.user.userprofile
        qs = locationdepartamentfilter(DocQuestion.objects,user)

        if self.request.GET.get('category') != None:
            query = self.request.GET.get('category')
            qs = qs.filter(Q(category=query))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = KnowledgeCategory.objects.all()
        return context


class UnansweredQuestionListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = UserQuestion
    permission_required = 'news.view_userquestion'
    template_name = "news/pending_questions.html"

#
# class QuestionUpdateView(UpdateView):
#     model = DocQuestion
#     form_class = DocQuestionForm
#     success_url = '/QandA/'
#
#     template_name = "news/upload.html"


class UnpublishedNewsListView(LoginRequiredMixin,
                                PermissionRequiredMixin, ListView):
    model = News
    permission_required = ('news.add_news',)

    def get_queryset(self):
        return News.objects.filter(published_date=None).order_by('-date_created')

class LocationDepartamentCheckMixin:

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if (request.user.userprofile.departament == self.object.target_departament
            or self.object.target_departament == 'non'):
            if (request.user.userprofile.location == self.object.target_location
                or self.object.target_location == 'non'):
                return super().dispatch(request, *args, **kwargs)
            else:
                return HttpResponseForbidden("403 Forbidden , you don't have access")
        else:
            return HttpResponseForbidden("403 Forbidden , you don't have access")


class NewsDetailView(LoginRequiredMixin, LocationDepartamentCheckMixin, DetailView):
    model = News


class DocDetailView(LoginRequiredMixin, LocationDepartamentCheckMixin, DetailView):
    model = DocumentF


class NewsListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = News

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['activate'] = NewsReadFlag.objects.filter(
    #         user=self.request.user, read=False).values_list('news', flat=True)
    #     return context

    def get_queryset(self):
        userprofile = self.request.user.userprofile
        qs = News.objects.exclude(published_date=None).order_by('-published_date')
        qs = locationdepartamentfilter(qs,userprofile)

        return qs

@login_required
@permission_required('news.add_news', raise_exception=True)
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

@login_required
@permission_required('news.view_userquestion', raise_exception=True)
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
@permission_required('news.add_news', raise_exception=True)
def publish_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    news.publish()
    return redirect('news:news_list')


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
@permission_required('news.add_documentf', raise_exception=True)
def post_document(request):
    if request.method == 'POST':
        form = DocumentFForm(request.POST)

        if form.is_valid():
            news_instance = form.save(commit=False)
            news_instance.author = User.objects.get(
                username=request.user.username)
            news_instance.save()
            return redirect('news:knowledge')
    else:
        form = DocumentFForm()
    return render(request, 'news/upload.html', {'form': form})


@login_required
@permission_required('news.add_docfile', raise_exception=True)
def post_file(request):
    if request.method == 'POST':
        form = DocFileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')
        for f in files:
            file_instance = form.save(commit=False)
            file_instance.isnews = False
            file_instance.save()
            return redirect('news:knowledge')
    else:
        form = DocFileForm()
    return render(request, 'news/upload.html', {'form': form})

@login_required
@permission_required('news.add_docquestion', raise_exception=True)
def post_question(request):
    if request.method == 'POST':
        form = DocQuestionForm(request.POST)

        if form.is_valid():
            news_instance = form.save(commit=False)
            news_instance.save()
            return redirect('news:faq')
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
            return redirect('news:faq')
    else:
        form = UserQuestionForm()
    return render(request, 'news/upload.html', {'form': form})
