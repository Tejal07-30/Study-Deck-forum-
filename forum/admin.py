from django.contrib import admin
from .models import Category, Thread, Reply, ReplyReport

admin.site.register(Category)
admin.site.register(Thread)
admin.site.register(Reply)
@admin.register(ReplyReport)
class ReplyReportAdmin(admin.ModelAdmin):
    list_display = ('reply', 'reported_by', 'created_at')
    search_fields = ('reason',)