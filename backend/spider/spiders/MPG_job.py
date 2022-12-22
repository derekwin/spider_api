__name__ = '马普所-德国'

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

BaseURL = "https://www.mpg.de/stellenboerse?job_type%5B%5D=sc&job_type%5B%5D=sc_jun"
base = "https://www.mpg.de/"
Tag = True

def get_data(driver, url):
    global Tag

    driver.get(url)
    time.sleep(2)
    
    has_button = True
    while has_button:
        button = driver.find_element(By.XPATH, '//*[@id="more-job-offers"]/span')
        if button.get_attribute("data-disabled") != "disabled":
            button.click()
            time.sleep(0.5)
        else:
            has_button = False

    content = driver.page_source
    # jobdivs = driver.find_element(By.ID, 'jobs')
    soup = BeautifulSoup(content, 'html.parser')
    jobdivs = soup.find("ul", id="show_more-jobs")
    jobs = jobdivs.contents

    items = []
    for job in jobs:
        item = {}
        try:
            # print(job.find("div", class_="text-box"))
            textbox = job.find("div", class_ ="text-box")
            # print(textbox.contents[0].contents[0].find("a").get('href'))
            item['title'] = textbox.find("h3").find("a").get_text().strip()
            if len(Position.objects.filter(title=item['title']))>0:
                print("pass")
                Tag = False
                continue
            if not Tag and len(Position.objects.filter(title=item['title']))==0:
                print("rerun")
                Tag = True
            item['college'] = "马普所"
            # .split('\n\n\n')[-1]
            item['academy'] = textbox.contents[1].get_text().strip()
            item['link'] = base + textbox.find("h3").find("a").get('href')
            item['deadline'] = "发布时间："+textbox.find("span", class_='date').get_text().strip()
            # # print(item)
            items.append(item)
        except Exception as e:
            # print(traceback.print_exc())
            continue
    return items


def main(driver):
    global Tag
    while Tag:
        latest_url = BaseURL
        print(f"findphd_job : {latest_url}, fetching")
        items = get_data(driver, latest_url)
        print(items)
        print(f"findphd_job : {latest_url}, fetching over")
        for i in items:
            print(f"insert new : {i['title']}")
            Position.objects.create(**i)
        print(f"findphd_job : {latest_url}, insert over")
        # page += 5
        Tag = False


def run(missionDb):
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # button = driver.find_element(By.XPATH, '//*[@id="more-job-offers"]/span')
        # button.get_attribute("data-disabled")
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