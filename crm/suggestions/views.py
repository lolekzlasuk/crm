
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Post, Comment, BoardCategory
from django.utils import timezone
from django.contrib import messages
from django.core.paginator import Paginator
# Create your views here.


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.order_by('-last_comment')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BoardCategory.objects.all()
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post


class CategoryDetailView(LoginRequiredMixin, ListView):
    model = BoardCategory

    template_name = 'suggestions/boardcategory_detail.html'

    def get_queryset(self, **kwargs):
        queryset = Post.objects.all().filter(
            category_id=self.kwargs['pk']).order_by('-last_comment')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = BoardCategory.objects.filter(
            pk=self.kwargs['pk'])
        context['categories'] = BoardCategory.objects.all()
        return context


@login_required
def post_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = User.objects.get(username=request.user.username)
            instance.save()
            return redirect('suggestions:Postlist')
    else:
        form = PostForm()
    return render(request, 'suggestions/Postform.html', {'form': form})


@login_required
def post_comment(request, pk):
    Post = get_object_or_404(Post, pk=pk)
    context = {}
    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            Post.last_comment = timezone.now()
            Post.save()
            instance = form.save(commit=False)
            instance.author = User.objects.get(username=request.user.username)
            instance.Post = Post
            instance.save()
            return redirect('suggestions:Postlist')
    else:
        form = CommentForm()
    return render(request, 'suggestions/commentform.html', {'form': form})
