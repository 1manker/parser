import sys
import time
import codecs
import subprocess as sub
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import os

url = str(sys.argv[1])
driver = webdriver.Chrome(executable_path="C://Program Files (x86)//Google//Chrome//chromedriver.exe")
driver.implicitly_wait(30)
driver.get(url)
options = Options()
options.headless = False


def click_to_end():
    more_button = driver.find_element_by_id("gsc_bpf_more")
    while more_button:
        more_button = driver.find_element_by_id("gsc_bpf_more")
        if not more_button.is_enabled():
            break
        more_button.click()
        time.sleep(1)


def find_author():
    soup = BeautifulSoup(driver.page_source, 'lxml')
    author_bulk = soup.find('div', attrs={"id": "gsc_prf_in"})
    this_author = author_bulk.text
    this_author = this_author.split(' ')
    this_author = this_author[1]
    return this_author


def find_paper_title():
    soup = BeautifulSoup(driver.page_source, 'lxml')
    paper_title = soup.find('a', attrs={"class": "gsc_vcd_title_link"})
    if paper_title is None:
        return ''
    else:
        return paper_title.text


def iterate_through_pages():
    while len(driver.find_elements_by_xpath("//*[@id='gs_nm']/button[2]")) != 0:
        page_button = driver.find_element_by_xpath("//*[@id='gs_nm']/button[2]").click()
        time.sleep(2)


def iterate_through_links():
    index = 1
    author = find_author()
    while len(driver.find_elements_by_xpath("//*[@id='gsc_a_b']/tr[" + str(index) + "]/td[1]/a")) != 0:
        citation_button = driver.find_element_by_xpath("//*[@id='gsc_a_b']/tr[" + str(index) + "]/td[1]/a")
        citation_button.click()
        time.sleep(2)
        title = find_paper_title()
        data_group = pull_data()
        exp_to_file(author, title, data_group)
        citation_button = driver.find_element_by_xpath("//*[@id='gs_md_cita-d-x']").click()
        time.sleep(2)
        index += 1
    return


def exp_to_file(name, this_title, arr):
    f = codecs.open("C://Users//Luke//Desktop//" + name + ".csv", "a+", "utf-8")
    for x in arr:
        f.write(this_title + "," + x + "\n")
    f.close()
    return


def pull_data():
    new_soup = BeautifulSoup(driver.page_source, 'lxml')
    dates = []
    cit_count = []
    data = []
    for x in new_soup.findAll('div', attrs={"id": "gsc_vcd_graph_bars"}):
        for y in x.findAll('a', href=True):
            temp = (y['href']).split("yhi=")
            dates.append(temp[1])
    for x in new_soup.findAll('span', attrs={"class": "gsc_vcd_g_al"}):
        cit_count.append(x.text)
    for x in range(len(dates)):
        data.append(dates[x] + "," + cit_count[x])
    return data


auth_name = find_author()
click_to_end()
time.sleep(1)
iterate_through_links()
driver.close()
time.sleep(10)
os.system('python combo.py ' + auth_name)


