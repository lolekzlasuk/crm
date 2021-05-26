from django.shortcuts import render, get_object_or_404,redirect
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View,TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from .models import UserProfile
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import logout
from .forms import UserProfileForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect
import os
from pathlib import Path

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })



class UserProfileDetailView(DetailView):
    model = UserProfile
    queryset = User.objects.all()
    def get_object(self):
        return self.request.user.userprofile

def user_logout(request):
    logout(request)
    return redirect('/')

class EmployeeListView(LoginRequiredMixin,ListView):
    paginate_by = 10
    model = UserProfile
    template_name = 'accounts/userprofile_list.html'
    def get_queryset(self):
        object_list = UserProfile.objects.all()
        if self.request.GET.get('q') != None:

            query = self.request.GET.get('q')
            object_list = UserProfile.objects.all().filter(
            Q(name__icontains=query) | Q(email__icontains=query) | Q(departament__icontains=query) | Q(location__icontains=query) | Q(position__icontains=query)
            )
        return object_list

    # def get_queryset(self):
    #     return Story.objects.order_by('-created_date')

#
# class EmployeeDetailView(DetailView):
#     model = UserProfile
#     def get_queryset(self):
#         queryset = request

# def ProfileView(request):
#     userr = request.user.userprofile
#
#     return userr
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                messages.success(request, 'Your password was updated successfully!')
                return HttpResponseRedirect(reverse('news:newss'))

            else:
                return HttpResponse('account no active')
        else:
            print('failed login detected')
            print('username: {} and password {}'.format(username,password))
            return HttpResponse('invalid login details supplied')

    else:
        return render(request,'accounts/login.html',{})


def edit_profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance = profile)
        prev_pic = profile.profile_pic
        perv_path = profile.profile_pic.path
        files = request.FILES.getlist('file')
        if form.is_valid():
            print('form valid')

            image = UserProfile.objects.resize_file(request.FILES['profile_pic'])

            profile.profile_pic = image
            profile.save()
            if prev_pic != "profile_pics/default-profile.png":
                if os.path.isfile(prev_pic.path):
                    os.remove(prev_pic.path)
        return redirect('accounts:profile')
    else:
        form = UserProfileForm
    return render(request,'accounts/editprofile.html',{'form':form})

def delete_profile_pic(request):
    profile = request.user.userprofile
    if request.user.userprofile.profile_pic != "profile_pics/default-profile.png":
        if os.path.isfile(profile.profile_pic.path):
            os.remove(profile.profile_pic.path)
        profile.profile_pic = "profile_pics/default-profile.png"
        profile.save()
        return redirect('accounts:profile')
