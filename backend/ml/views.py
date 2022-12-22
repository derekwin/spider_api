from django.shortcuts import render
from findphd.models import Position

# Create your views here.

# Todo.
def getitem(request):
    itemlist = Position.objects.filter(type=None)
    itemlist.count()
    context = {'count':itemlist.count}
    return render(request, 'ml/mission.html', context)