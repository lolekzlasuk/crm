import datetime
import crm.Calendary.models
start_date = datetime.date(2020, 2, 2)
end_date   = datetime.date(2022, 2, 2)
dates = [ start_date + datetime.timedelta(n) for n in range(int ((end_date - start_date).days))]

for each in dates:
    Day.objects.create(date=each)
