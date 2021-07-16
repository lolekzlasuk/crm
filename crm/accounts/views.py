from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DetailView
from .models import UserProfile
import random
import string
from django.utils import timezone
from django.db.models import Q
from .forms import UserProfileForm,  CreateProfileForm, UserForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, \
    login, logout
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required, permission_required
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        return context


@login_required
def user_logout(request):
    logout(request)
    return redirect('/')


class EmployeeListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'accounts/userprofile_list.html'
    paginate_by = 9

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact List'
        return context


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

        if form.is_valid():
            profile.change_profile_pic(request.FILES['profile_pic'])
        return redirect('accounts:profile')
    else:
        form = UserProfileForm

    return render(request, 'accounts/editprofile.html', {
        'form': form, 'title': 'Password Change'})


@login_required
def delete_profile_pic(request):
    profile = request.user.userprofile
    profile.set_default_profile_pic()

    return redirect('accounts:profile')

@login_required
@permission_required('users.add_user', raise_exception=True)
def register(request):

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = CreateProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()
            rand_string = ''.join(random.choices( \
                        string.ascii_letters + string.digits, k=15))
            user.set_password(rand_string)
            user.save()

            profile = profile_form.save(commit=False)
            profile.email = user.email
            profile.user = user
            profile.save()

            return redirect('news:news_list')
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = CreateProfileForm()

    return render(request,'accounts/registration.html',
                            {'user_form':user_form,
                            'profile_form':profile_form})

def set_password(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            user.userprofile.is_active = True
            user.userprofile.save()
            messages.success(
                request, 'Your password was successfully set!')
            return redirect('news:news_list')
        else:
            messages.error(request, 'Please correct the error below.')
    elif request.user.userprofile.is_active == True:
        return redirect('news:news_list')
    elif request.user.userprofile.is_active == False:
        form = SetPasswordForm(request.user)
    return render(request, 'accounts/set_password.html', {
        'form': form
    })

def first_login(request, string):
    user = User.objects.get(userprofile__first_login_string = string)
    if user.userprofile.is_active == True:
        return HttpResponseForbidden()
    else:
        login(request, user)
        return HttpResponseRedirect(reverse('accounts:set_password'))
