from django.contrib.auth.models import User
from django.db import models
from pygments import highlight
from pygments.formatters.html import HtmlFormatter
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Group(models.Model):
    name = models.TextField()
    priority = models.IntegerField()
    color = models.CharField(max_length=7)

    class Meta:
        unique_together = (('id', 'name'),)
        ordering = ('priority',)


class Reference(models.Model):
    name = models.TextField()
    url = models.URLField()
    group = models.ForeignKey('Group', related_name='groups', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='references', on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)
