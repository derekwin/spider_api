__name__ = 'jobbnorge-挪威'

import time
from spider.models import Mission
from findphd.models import Position
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import traceback

BaseURL = "https://www.jobbnorge.no/search/en?OrderBy=Published&Period=All&category=35"

Tag = True

def get_data(driver, url):
    global Tag

    driver.get(url)
    time.sleep(5)
    content = driver.page_source
    # jobdivs = driver.find_element(By.ID, 'jobs')
    soup = BeautifulSoup(content, 'html.parser')
    jobs_divs = soup.find("div", id='jobs')
    jobs = jobs_divs.contents

    items = []
    for job in jobs:
        item = {}
        try:
            item['title'] = job.find("span", itemprop='title').get_text().strip()
            if len(Position.objects.filter(title=item['title']))>0:
                print("pass")
                Tag = False
                continue
            if not Tag and len(Position.objects.filter(title=item['title']))==0:
                print("rerun")
                Tag = True
            item['college'] = job.find("span", itemprop='hiringOrganization').get_text().strip()
            item['link'] = job.find("h2", class_='h3').find("a").get('href')
            item['detail'] = job.find("p", class_='hide-for-small-only').get_text().strip()
            item['academy'] = job.find("p", class_='employment-position').get_text().strip()
            item['research_type'] = job.find("p", class_='employment-time').get_text().strip()
            item['deadline'] = job.find("p", class_='employment-type').get_text().strip()
            # print(item)
            items.append(item)
        except:
            continue
    return items


def main(driver):
    global Tag
    page = 5
    while Tag:
        latest_url = BaseURL + f"#{page}"
        print(f"findphd_job : {page} page, fetching")
        items = get_data(driver, latest_url)
        print(f"findphd_job : {page} page, fetching over")
        for i in items:
            print(f" {page} page, insert new : {i['title']}")
            Position.objects.create(**i)
        print(f"findphd_job : {page} page, insert over")
        page += 5
        Tag = False


def run(missionDb):
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        missionDb.status = Mission.Status.R
        missionDb.save()
        main(driver)
        driver.close()
        missionDb.status = Mission.Status.NR
        missionDb.save()
    except Exception as e:
        print(e)
        driver.close()
        missionDb.status = Mission.Status.ER
        missionDb.save()
        print(traceback.print_exc())


# https://www.jobbnorge.no/search/en?OrderBy=Published&Period=All&category=35#7
# 研究工作 - 分类