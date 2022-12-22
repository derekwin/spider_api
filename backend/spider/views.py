from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
from spider.models import Mission
from spider.spiders import *
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime
import pytz

all = Mission.objects.all()
for i in all:
    if i.title not in spiders_list:
        i.delete()

for i in spiders_list:
    if Mission.objects.filter(title=i.__name__):
        pass
    else:
        item = Mission.objects.create(title=i.__name__)
    # Mission.objects.filter(title=i.__name__).delete()

sched = BackgroundScheduler()
sched.start()

# Create your views here.

# 任务执行动作 

@login_required(login_url='/admin/login')
def getmission(request):
    data = []
    for index, item in enumerate(spiders_list):
        missionDb = Mission.objects.get(title=item.__name__)
        # is_today = False
        # if missionDb.last_time.replace(tzinfo=pytz.timezone('PRC')).day == datetime.today().replace(tzinfo=pytz.timezone('PRC')).day:
        #     is_today = True
        data.append({
            'id':index,
            'title':item.__name__,
            'status':missionDb.status,
            'last_time':missionDb.last_time,
            'is_today': missionDb.last_time.replace(tzinfo=pytz.timezone('PRC')).day == datetime.today().replace(tzinfo=pytz.timezone('PRC')).day
        })
    context = {'data':data,'maxnum':len(spiders_list)+1}
    return render(request, 'spider/mission.html', context)

@login_required(login_url='/admin/login')
@permission_required(('findphd.add_position', 'findphd.delete_position', 'findphd.change_position', 'findphd.view_position'), login_url='/admin/login')
def execmission(request, id:int):
    if request.method == 'POST':
        if id<len(spiders_list):
            mission = spiders_list[id]
            missionDb = Mission.objects.get(title=mission.__name__)
            sched.add_job(mission.run, args=[missionDb])
            return HttpResponse('success')
        elif id == len(spiders_list)+1:  # run all
            for i in spiders_list:
                missionDb = Mission.objects.get(title=i.__name__)
                sched.add_job(i.run, args=[missionDb])
                time.sleep(1)
            return HttpResponse('success')
        else:
            return HttpResponseForbidden('error')
    else:
        return HttpResponseForbidden('error')

# 结果审核动作