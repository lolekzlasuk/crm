from django.contrib import admin


from .models import News,NewsFile,Notification,NotificationReadFlag,NewsReadFlag,KnowledgeCategory
# Register your models here.
admin.site.register(News)
admin.site.register(NewsReadFlag)
admin.site.register(Notification)
admin.site.register(NotificationReadFlag)
admin.site.register(NewsFile)
admin.site.register(KnowledgeCategory)
