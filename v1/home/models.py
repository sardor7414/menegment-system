from django.db import models
import random

# Create your models here.

class DefaultAbstract(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Board(DefaultAbstract):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '1) Boards'

class Column(DefaultAbstract):
    title = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_columns')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '2) Columns'


class Task(DefaultAbstract):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, blank=True, null=True, related_name='column_tasks')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '3) Tasks'



class BoardMember(DefaultAbstract):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_member')
    user = models.ForeignKey('user.user', on_delete=models.CASCADE, related_name='board_member')
    inviter = models.ForeignKey('user.user', on_delete=models.CASCADE, related_name='board_inviter')
    token = models.CharField(max_length=255)
    code = models.CharField(max_length=4)
    is_success = models.BooleanField(default=False)

    class Meta:
        unique_together = ('board', 'user', 'is_success')




