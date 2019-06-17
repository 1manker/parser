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

connection = mysql.connector.connect(
        host="uwyobibliometrics.hopto.org",
        database="bibliometrics",
        user="luke",
        password="1234",
        auth_plugin="mysql_native_password"
    )
finished = False
sql_query = "select * from linkqueue"
cursor = connection.cursor(prepared=True)
cursor.execute(sql_query)
results = cursor.fetchall()
if len(results) < 1:
    finished = True
while not finished:
    time.sleep(5)
    os.system('python authorScrape.py ' + "https://scholar.google.com/citations?user=" + results[0])
    f = codecs.open("C://Users//Luke//Desktop//combo1.csv", "r", "utf-8")
    for line in f:
        temp = line.split(",")
        sql_insert = "insert into citations values(%s, %s, %s)"
        if len(temp) > 1:
            input_strings = (temp[0], temp[1], temp[2].rstrip())
            cursor.execute(sql_insert, input_strings)
    f.close()
    time.sleep(2)
    f = open("C://Users//Luke//Desktop//combo1.csv", "w+")
    f.truncate(0)
    f.close()
    connection.commit()
    sql_drop = ("delete from linkqueue where link = " + results[0],)
    cursor.execute(sql_drop)
    sql_add = "insert into linksearched values(" + results[0] + ")"
    cursor.execute(sql_add)
    connection.commit()
    results = cursor.fetchall()
    if len(results) < 1:
        finished = True
connection.close()
