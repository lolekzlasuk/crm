from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import UserProfile
from django.utils import timezone
from django.db.models import Q
from .forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })


class UserProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user.userprofile

@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


class EmployeeListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'accounts/userprofile_list.html'
    paginate_by = 20

    def get_queryset(self):
        object_list = UserProfile.objects.all()
        if self.request.GET.get('q') != None:
            query = self.request.GET.get('q')

            object_list = UserProfile.objects.all().filter(
                Q(name__icontains=query) | Q(email__icontains=query)
                | Q(departament__icontains=query) | Q(location__icontains=query)
                | Q(position__icontains=query) | Q(telephone__icontains=query)
            )

        return object_list


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Logged in!')
                return HttpResponseRedirect(reverse('news:news_list'))
            else:
                return HttpResponse('Account is not active')
        else:
            print('failed login detected')
            print('username: {} login failed'.format(username))
            return HttpResponse('invalid login details supplied')

    else:
        return render(request, 'accounts/login.html', {})

@login_required
def edit_profile(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        files = request.FILES.getlist('file')

        if form.is_valid():
            profile.change_profile_pic(request.FILES['profile_pic'])
        return redirect('accounts:profile')
    else:
        form = UserProfileForm
    return render(request, 'accounts/editprofile.html', {'form': form})

@login_required
def delete_profile_pic(request):
    profile = request.user.userprofile
    profile.set_default_profile_pic()


    return redirect('accounts:profile')
