from django.contrib import admin


from .models import News,NewsFile,Notification,NotificationReadFlag,NewsReadFlag,KnowledgeCategory,DocFile,DocumentF
# Register your models here.
admin.site.register(News)
admin.site.register(NewsReadFlag)
admin.site.register(Notification)
admin.site.register(NotificationReadFlag)
admin.site.register(NewsFile)
admin.site.register(KnowledgeCategory)
admin.site.register(DocFile)
admin.site.register(DocumentF)
