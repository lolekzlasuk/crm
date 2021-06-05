from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.contrib.auth.models import User
from accounts.models import UserProfile
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from .models import Day, Devent
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q
from .forms import DeventForm


class DeventDetailView(DetailView):
    model = Devent


class CalListView(ListView):
    model = Day

    def get_queryset(self):
        qs = Day.objects.filter(
            date__month=self.kwargs['month']
        ).filter(
            date__year=self.kwargs['year']
        )

        dayrange = qs[0].date.weekday()
        list_of_pks = list(range(qs[0].pk - dayrange, qs[0].pk))
        qp = Day.objects.filter(pk__in=list_of_pks)
        cq = qs.union(qp)

        lastday = qs[len(qs) - 1].date.weekday()
        list_of_top_pks = list(
            range(qs[len(qs) - 1].pk,
                  qs[len(qs) - 1].pk + 7 - lastday)
        )
        ql = Day.objects.filter(pk__in=list_of_top_pks)
        qq = cq.union(ql)

        return qq

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Day.objects.filter(
            date__month=self.kwargs['month']
        ).filter(
            date__year=self.kwargs['year']
        )

        alldays = len(qs) + qs[0].date.weekday()

        context['before'] = qs[0].date.weekday()
        context['after'] = alldays + 1
        context['date'] = datetime.date(
            self.kwargs['year'], self.kwargs['month'], 1).strftime("%B %Y")

        if self.kwargs['month'] == 12:
            context['nextmonth'] = 1
            context['nextyear'] = self.kwargs['year'] + 1
        elif self.kwargs['month'] != 12:
            context['nextmonth'] = self.kwargs['month'] + 1
            context['nextyear'] = self.kwargs['year']

        if self.kwargs['month'] == 1:
            context['prevmonth'] = 12
            context['prevyear'] = self.kwargs['year'] - 1
        elif self.kwargs['month'] != 1:
            context['prevmonth'] = self.kwargs['month'] - 1
            context['prevyear'] = self.kwargs['year']

        return context


@login_required
def post_devent(request, pk):
    data = {"start": "00:00", "end": "23:59"}
    if request.method == 'POST':
        Days = get_object_or_404(Day, pk=pk)
        form = DeventForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = User.objects.get(username=request.user.username)
            instance.day = Days
            instance.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = DeventForm(initial=data)
    return render(request, 'calendary/deventform.html', {'form': form})
