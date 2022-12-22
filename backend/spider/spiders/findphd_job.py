__name__ = 'findphd-英国'

import time
from spider.models import Mission
from findphd.models import Position
import requests
from bs4 import BeautifulSoup
import traceback

BaseURL = "https://www.findaphd.com"
Tag = True

def get_data(url):
    global Tag
    data = requests.get(url, timeout=10)
    soup = BeautifulSoup(data.text, 'html.parser')
    divs = soup.find_all("div", class_="resultsRow phd-result-row-standard phd-result row py-2 w-100 px-0 m-0")
    items = []
    for i in divs:
        item = {}
        try:
            item['title'] = i.find("a", class_="h4 text-dark mx-0 mb-3").text
            if len(Position.objects.filter(title=item['title']))>0:
                print("pass")
                Tag = False
                continue
            if not Tag and len(Position.objects.filter(title=item['title']))==0:
                print("rerun")
                Tag = True
            item['college'] = i.find("a", class_="instLink col-24 px-0 col-md-auto phd-result__dept-inst--inst phd-result__dept-inst--title h6 mb-0 text-secondary font-weight-lighter").get("title")
            item['academy'] = i.find("a", class_="col-24 px-0 col-md-auto deptLink phd-result__dept-inst--dept phd-result__dept-inst--title h6 mb-0 text-secondary font-weight-lighter").get_text()
            item['link'] = BaseURL + i.find("a", class_="phd-result__description--read-more text-secondary text-nowrap").get("href")
            item['supervisors'] = i.find("a", class_="phd-result__key-info super text-wrap badge badge-light card-badge p-2 m-1 font-weight-light").contents[1].contents[2].get_text()
            threeitems = i.find("div", class_="phd-icon-area mx-n1")
            item['deadline'] = threeitems.contents[1].contents[0].get_text()
            item['research_type'] = threeitems.contents[3].contents[0].get_text()
            item['fund_type'] = threeitems.contents[5].contents[0].get_text()
            
            item['detail'] = ''
            detail_data = requests.get(item['link'], timeout=10)
            detail_soup = BeautifulSoup(detail_data.text, 'html.parser')
            detailitem = detail_soup.find("div", class_="phd-sections phd-sections__description row mx-0 ml-md-n3 mr-md-0 my-3")
            if detailitem:
                item['detail'] = item['detail'] + detailitem.get_text() + "\n"
            detailitem = detail_soup.find("div", class_="phd-sections phd-sections__funding-notes row mx-0 ml-md-n3 mr-md-0 my-3 overflow-hidden")
            if detailitem:
                item['detail'] = item['detail'] + detailitem.get_text() + "\n"
            detailitem = detail_soup.find("div", class_="pphd-sections phd-sections__references row mx-0 ml-md-n3 pr-md-0 my-3 overflow-hidden")
            if detailitem:
                item['detail'] = item['detail'] + detailitem.get_text() + "\n"
            # item['contact'] = i.find("a", class_="phd-result__description--read-more text-secondary text-nowrap").get("href")
            # cant get now
            items.append(item)
        except Exception:
            continue
    return items


def main():
    page = 1
    max = 10
    while Tag and page < max:
        latest_url = BaseURL + f"/phds/latest/?PG={page}"
        print(f"findphd_job : {page} page, fetching")
        items = get_data(latest_url)
        print(f"findphd_job : {page} page, fetching over")
        for i in items:
            print(f" {page} page, insert new : {i['title']}")
            Position.objects.create(**i)
        print(f"findphd_job : {page} page, insert over")
        page += 1
    

def run(missionDb):
    try:
        missionDb.status = Mission.Status.R
        missionDb.save()
        # Position.objects.all().delete()
        main()
        missionDb.status = Mission.Status.NR
        missionDb.save()
    except Exception as e:
        print(e)
        print(traceback.print_exc())
        missionDb.status = Mission.Status.ER
        missionDb.save()