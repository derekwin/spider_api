from django.urls import path
from spider.views import getmission, execmission

urlpatterns = [
    path('', getmission),
    path('exec/<int:id>', execmission),
]
