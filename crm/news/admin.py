from django.contrib import admin


from .models import *
# Register your models here.
admin.site.register(News)
admin.site.register(Notification)
admin.site.register(NotificationReadFlag)
admin.site.register(NewsFile)
admin.site.register(KnowledgeCategory)
admin.site.register(DocFile)
admin.site.register(DocumentF)
admin.site.register(DocQuestion)
admin.site.register(UserQuestion)
