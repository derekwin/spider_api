from django.contrib import admin
from findphd.models import Position, User, Post
# Register your models here.

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'title_zh', 'deadline', 'supervisors', 'link')
    search_fields = ('title', 'title_zh', 'deadline', 'supervisors', 'detail', 'detail_zh')
    list_filter = ('deadline',)
    ordering = ('-id',)
    # fields = ('title',) # 编辑字段
    # exclude = ('country',) # 排除字段

# admin.site.register(User)
@admin.register(User)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'code')
    ordering = ('-id',)

# admin.site.register(Post)
@admin.register(Post)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('to', 'creator', 'detail', 'timestamp')
    ordering = ('-id',)