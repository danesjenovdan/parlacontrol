from django.contrib import admin

from dashboard.models import Group, Setter, Status, Cron, ActiveCron
# Register your models here.

admin.site.register(Group)
admin.site.register(Setter)
admin.site.register(Status)
admin.site.register(Cron)
admin.site.register(ActiveCron)