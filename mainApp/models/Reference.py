from django.db import models


class Reference(models.Model):
    name = models.TextField()
    ref_url = models.URLField()
    group = models.ForeignKey(
            'Group',
            related_name='groups',
            on_delete=models.CASCADE,
            blank=True,
            null=True
    )
    user = models.ForeignKey(
            'User',
            related_name='references',
            on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('id',)
