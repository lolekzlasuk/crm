from django.contrib import admin

from .models import Poll,Question,Answer,PollSubmition,PollSubmitionQuestion
# Register your models here.
admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(PollSubmition)
admin.site.register(PollSubmitionQuestion)
