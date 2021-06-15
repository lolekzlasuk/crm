from django.shortcuts import render, get_object_or_404, redirect
import datetime
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Day, Devent
from .forms import DeventForm
from django.contrib.auth.decorators import permission_required


class DeventDetailView(LoginRequiredMixin, DetailView):
    model = Devent


class DayListView(LoginRequiredMixin, ListView):
    model = Day

    def get_queryset(self):
        qs = Day.objects.filter(date__month=self.kwargs['month']
            ).filter(date__year=self.kwargs['year'])

        # appending proper amount of days from previous and next months to create a square in template
        first_day_weekday = qs[0].date.weekday()
        list_of_pks_days_before = list(range(qs[0].pk - first_day_weekday, qs[0].pk))
        qs_days_before = Day.objects.filter(pk__in=list_of_pks_days_before)
        qs_days_days_before = qs.union(qs_days_before)

        last_day_weekday = qs[len(qs) - 1].date.weekday()
        list_of_pks_days_ahead = list(
            range(qs[len(qs) - 1].pk,
                  qs[len(qs) - 1].pk + 7 - last_day_weekday))
        qs_days_ahead = Day.objects.filter(pk__in=list_of_pks_days_ahead)
        qs_padded_days = qs_days_days_before.union(qs_days_ahead)

        return qs_padded_days

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = Day.objects.filter(date__month=self.kwargs['month']
            ).filter(date__year=self.kwargs['year'])

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
@permission_required('calendary.add_devent', raise_exception=True)
def post_devent(request, pk):
    username = request.user.username
    data = {"start": "00:00", "end": "23:59"}
    if request.method == 'POST':
        Days = get_object_or_404(Day, pk=pk)
        form = DeventForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = User.objects.get(username=username)
            instance.day = Days
            instance.save()
            month = instance.day.date.month
            year = instance.day.date.year
            return redirect('calendary:calendary', month=month, year=year)
    else:
        form = DeventForm(initial=data)
    return render(request, 'calendary/deventform.html', {'form': form})
