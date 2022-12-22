from django.urls import path
from ml.views import getitem

urlpatterns = [
    path('', getitem),
]
