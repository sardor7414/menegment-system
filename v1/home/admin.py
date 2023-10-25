from django.contrib import admin
from .models import Board, Column, Task, BoardMember

# Register your models here.
@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'created_at')


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'column', 'created_at')



@admin.register(BoardMember)
class BoardMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'board', 'user', 'inviter', 'created_at')