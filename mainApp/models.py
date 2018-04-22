from django.contrib.auth.models import AbstractUser, User as default_user
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from rest_framework import renderers
from rest_framework.decorators import action
from rest_framework.response import Response

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class User(AbstractUser):

    def __str__(self):
        return self.username


class Group(models.Model):
    name = models.TextField()
    priority = models.IntegerField()
    color = models.CharField(max_length=7)
    user = models.ForeignKey('User', related_name='groups_ref', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('id', 'name'),)
        ordering = ('priority',)


class Reference(models.Model):
    name = models.TextField()
    ref_url = models.URLField()
    group = models.ForeignKey(Group,
                              related_name='groups',
                              on_delete=models.CASCADE,
                              blank=True,
                              null=True
                              )
    user = models.ForeignKey('User', related_name='references', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
