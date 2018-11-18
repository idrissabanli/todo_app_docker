from django.contrib import admin
from .models import Tasks, TaskReviews, SharingTasks
# Register your models here.


admin.site.register(Tasks)
admin.site.register(TaskReviews)


class SharingTaskAdmin(admin.ModelAdmin):
    model = SharingTasks
    list_display = ('task', 'user', 'sharing_type')


admin.site.register(SharingTasks, SharingTaskAdmin)