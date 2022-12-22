from django.db import models
from django.utils.translation import gettext_lazy as _

class Position(models.Model):
    class typeChoice(models.TextChoices):
        Li = 'Li', _('理学类')
        Go = 'Go', _('工程类')
        No = 'No', _('农学类')
        Ji = 'Ji', _('金融类')
        Ga = 'Ga', _('管理类')
        Yi = 'Yi', _('医学类')
        YS = 'YS', _('艺术类')

    type = models.CharField(
        max_length=2,
        choices=typeChoice.choices,
        default=None,
        null=True,
        blank=True
    )
    title = models.CharField(max_length=300, null=True, blank=True)
    title_zh = models.CharField(max_length=300, null=True, blank=True)
    college = models.CharField(max_length=80, null=True, blank=True)
    academy = models.CharField(max_length=200, null=True, blank=True)
    contact = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    deadline = models.CharField(max_length=30, null=True, blank=True)
    supervisors = models.CharField(max_length=80, null=True, blank=True)
    research_type = models.CharField(max_length=30, null=True, blank=True)
    fund_type = models.CharField(max_length=80, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    detail_zh = models.TextField(null=True, blank=True)
    link = models.CharField(max_length=500, null=True, blank=True)

class User(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    like = models.ManyToManyField(Position, related_name="Position")

    def __str__(self) -> str:
        return self.email

class Post(models.Model):
    detail = models.TextField()
    to = models.ForeignKey('self', related_name="post", blank=True, null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(User, related_name="creator", null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    best = models.CharField(max_length=1, null=True, blank=True) # T or F 加精

    def __str__(self) -> str:
        return self.detail