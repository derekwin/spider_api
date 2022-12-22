from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

# Create your models here.

class Mission(models.Model):
    title = models.CharField(max_length=20)

    class Status(models.TextChoices):
        NR = 'NR', _('NotRunning')
        R = 'R', _('Running')
        ER = 'ER', _('Error')

    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.NR,
    )

    last_time = models.DateTimeField(auto_now=True)