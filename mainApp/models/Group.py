from django.db import models

class Group(models.Model):
    name = models.TextField()
    priority = models.IntegerField()
    color = models.CharField(max_length=7)
    user = models.ForeignKey(
            'User',
            related_name='groups_ref',
            on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (('id', 'name'),)
        ordering = ('priority',)
