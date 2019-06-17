import sys
import time
import subprocess as sub
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


output_file_list = []


def printer(arr1, arr2, auth_name):
    author_string = "C:\\Users\\Luke\\Desktop\\" + auth_name + ".txt"
    file = open(author_string, "w+")
    output_file_list.append(author_string)
    for i in range(len(arr1)):
        if arr1[i] and arr2[i] and auth_name:
            file.write(auth_name + "," + arr1[i] + "," + arr2[i] + "\n", )


def scrape():
    cit_row = []
    author_row = []
    year_row = []
    name = ''
    for row in soup.findAll('div', attrs={"id": "gsc_prf_in"}):
        name = row.text
    for row in soup.findAll('a', attrs={"class": "gsc_a_ac gs_ibl"}):
        cit_row.append(row.text)
    for row in soup.findAll('a', attrs={"class": "gsc_a_at"}):
        author_row.append(row.text)
    for row in soup.findAll('span', attrs={"class": "gsc_a_h gsc_a_hc gs_ibl"}):
        year_row.append(row.text)
    printer(cit_row, year_row, name)


for x in range(len(sys.argv) - 1):
    url = str(sys.argv[x + 1])
    driver = webdriver.Chrome(executable_path="C://Program Files (x86)//Google//Chrome//chromedriver.exe")
    driver.implicitly_wait(30)
    driver.get(url)

    python_button = driver.find_element_by_id("gsc_bpf_more")
    while python_button:
        python_button = driver.find_element_by_id("gsc_bpf_more")
        if not python_button.is_enabled():
            break
        python_button.click()
        time.sleep(1)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    driver.close()
    scrape()

for k in range(len(output_file_list)):
    input_file = open(output_file_list[k])
    comb_file = open("C:\\Users\\Luke\\Desktop\\combo1.csv", "a")
    if k == 0:
        comb_file.write("Author,Citation_Count,Year" + "\n")
    comb_file.write(input_file.read())
    input_file.close()
    comb_file.close()

sub.Popen([r"C://Program Files//R//R-3.6.0//bin//x64//Rscript",
           "C://Users//Luke//Desktop//summer19 Research//graphScript.r"], shell=True)
