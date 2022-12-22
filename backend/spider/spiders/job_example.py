__name__ = 'cust'

import time
from spider.models import Mission

def main():
    print(__name__)
    time.sleep(10)
    print(__name__)
    pass

def run(missionDb):
    try:
        missionDb.status = Mission.Status.R
        missionDb.save()
        main()
        missionDb.status = Mission.Status.NR
        missionDb.save()
    except:
        missionDb.status = Mission.Status.ER
        missionDb.save()
    