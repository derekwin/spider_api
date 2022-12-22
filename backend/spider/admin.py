from django.contrib import admin
from spider.models import Mission
# Register your models here.

@admin.register(Mission)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'last_time')
    search_fields = ('title', 'status', 'last_time') 
    # list_filter = ('deadline',)
    # ordering = ('-id',)
    # fields = ('title',) # 编辑字段
    # exclude = ('country',) # 排除字段