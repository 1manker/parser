import sys
import time
import codecs
import subprocess as sub
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import mysql.connector
import os
import subprocess

connection = mysql.connector.connect(
        host="uwyobibliometrics.hopto.org",
        database="bibliometrics",
        user="luke",
        password="1234",
        auth_plugin="mysql_native_password"
    )
finished = False
sql_query = "select link from profiles where queue_status = false and search_status = false"
cursor = connection.cursor(prepared=True)
cursor.execute(sql_query)
results = cursor.fetchall()
time.sleep(5)
add_q_flag = "update profiles set queue_status = true where link = %s"
link = results[0][0].decode("utf-8")
sql_input = (link,)
cursor.execute(add_q_flag, sql_input)
connection.commit()
connection.close()

code = os.system('python ' + 'authorScrape.py ' + "https://scholar.google.com/citations\?user=" + results[0][0].decode("utf-8"))

print(code)
