from django.contrib import admin

from dashboard.models import Group, Setter, Status
# Register your models here.

admin.site.register(Group)
admin.site.register(Setter)
admin.site.register(Status)