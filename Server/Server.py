# importing libraries
import datetime
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import multiprocessing
import threading
import time
import pandas as pd
import pickle
import mysql.connector as ms
import yagmail

# loading cookies

cookie2 = []
cookie1 = []
cookies_ = pickle.load(open("fb.pkl", "rb"))
for cookie in cookies_:
    cookie2.append(cookie)
cookies_ = pickle.load(open("insta.pkl", "rb"))
for cookie in cookies_:
    cookie1.append(cookie)
curr_data = []
active_data = []
pending_task = []


# Function for sending email
def emai(active_data):
    yag = yagmail.SMTP(user="prodigy.tii@gmail.com", password="omnmh2003shubh")
    # sending the email
    for i in active_data:
        try:
            yag.send(to=i["email"], subject="Prodigy Reminder", contents=i["task"])
            print("Email sent successfully")
        except:
            print("Email Error")
            pass


# function for facebook
def facebook(active_data, cookie):

    chrome_options = Options()

    # initializing the selenium browser
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path="chromedriver.exe", options=chrome_options
    )
    print("Getting Link!")
    driver.get("https://www.facebook.com")
    m = [driver.add_cookie(i) for i in cookie]
    # print("Sending message!")
    # Iterating over given data
    for i in active_data:
        driver.get(f"https://www.facebook.com/messages/t/{i['fb']}")

        element = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    '//div[@data-contents="true"]//div[@data-block="true"]',
                )
            )
        )
        element.send_keys(i["task"])
        element.send_keys(Keys.ENTER)
        # print("Done")
    driver.close()
    return


# function for instagram
def instagram(active_data, cookie):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path="chromedriver.exe", options=chrome_options
    )
    # print("Initiating")
    driver.get("https://instagram.com")
    m = [driver.add_cookie(i) for i in cookie]
    # print("Login Successfull")
    # iterating over given data
    for i in active_data:
        driver.get(f"https://www.instagram.com/{i['insta']}")
        print("Sending Message")
        element = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//button[@type="button"][text()="Message"]')
            )
        )
        element.click()
        element = WebDriverWait(driver, 100).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//textarea[@placeholder="Message..."]')
            )
        )
        element.send_keys(i["task"])
        element.send_keys(Keys.ENTER)
        print("Completed!")
    # Waiting for message to be sent
    while True:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.elements_to_be_clickable(
                    (By.XPATH, '//div[@class="FeN85  xTVtN aQWyo"]')
                )
            )
        except:
            break
            driver.close()
        return


def connector(curr_data):
    global fields, pending_task, active_data, db, cursor, cookie1, cookie2, instagram, facebook
    temp_list = []
    all_done = []

    while True:
        # Connecting to database
        try:
            db = ms.connect(
                host="logs.c7xtjtjv8ph3.ap-south-1.rds.amazonaws.com",
                port=3306,
                user="shubh",
                passwd="shubh2003",
                db="tasker",
            )
            cursor = db.cursor()
            cursor.execute(
                "select users.*,task.date,task.time,task.task from users,task where DATE(task.date)=DATE(NOW()) and task.name=users.name order by task.time;"
            )
            b = cursor.fetchall()
            if len(b) > len(curr_data):
                cursor.execute(
                    "select users.*,task.date,task.time,task.task from users,task where DATE(task.date)=DATE(NOW()) and task.name=users.name order by task.time;"
                )
                fields = cursor.column_names
                temp = []
                while True:
                    try:
                        temp.append(dict(zip(cursor.column_names, cursor.fetchone())))
                    except:
                        break
                for j in temp:
                    for k in fields:
                        if j[k] == None:
                            j[k] = ""
                        else:
                            j[k] = str(j[k])
                for i in temp:
                    if i not in curr_data:
                        curr_data.append(i)
                print(
                    f"Statistics:\nAll tasks for the day:\n{pd.DataFrame.from_dict(curr_data)}"
                )
                active_task = [
                    i
                    for i in curr_data
                    if i["time"] == datetime.datetime.now().strftime("%H:%M:00")
                ]
                active_task = [i for i in active_task if i not in all_done]
                for i in active_task:
                    all_done.append(i)
                if len(active_task) > 0:
                    print("Starting Tasks:")
                    active_task = active_task[::-1]
                    print(f"{pd.DataFrame.from_dict(active_task)}")
                    a = active_task
                    insta_task = multiprocessing.Process(
                        target=instagram, args=(active_task, cookie1)
                    )
                    fab_task = multiprocessing.Process(
                        target=facebook, args=(active_task, cookie2)
                    )
                    ema_task = multiprocessing.Process(target=emai, args=(active_task,))
                    insta_task.daemon = True
                    fab_task.daemon = True
                    ema_task.daemon = True
                    insta_task.start()
                    fab_task.start()
                    ema_task.start()
                    active_task.clear()
                    print("startttt")
                    continue
            else:
                active_task = [
                    i
                    for i in curr_data
                    if i["time"] == datetime.datetime.now().strftime("%H:%M:00")
                ]
                active_task = [i for i in active_task if i not in all_done]
                for i in active_task:
                    all_done.append(i)
                if len(active_task) > 0:
                    print("Starting Tasks:")
                    active_task = active_task[::-1]
                    print(f"{pd.DataFrame.from_dict(active_task)}")
                    a = active_task
                    insta_task = multiprocessing.Process(
                        target=instagram, args=(active_task, cookie1)
                    )
                    fab_task = multiprocessing.Process(
                        target=facebook, args=(active_task, cookie2)
                    )
                    insta_task.daemon = True
                    fab_task.daemon = True
                    insta_task.start()
                    fab_task.start()
                    active_task.clear()
                    print("startttt")
                    continue
        except Exception as e:
            with open("error_log.txt", "a+") as f:
                f.write(str(e))
                f.write("\n")
            print("Exception")
            continue


def time_checker(curr_data, active_data, pending_task):
    print("Started 1")
    global fields
    temp = [
        i
        for i in curr_data
        if i["time"] == datetime.datetime.now().strftime("%H:%M:00")
    ]
    for i in temp:
        if i not in pending_task:
            pending_task.append(i)
            active_data.append(i)
    starter(active_data, curr_data)


def startert(insta, fb, active_data, curr_data):
    global cookie1, cookie2
    insta_task = multiprocessing.Process(target=insta, args=(active_data, cookie1))
    fab_task = multiprocessing.Process(target=fb, args=(active_data, cookie2))
    insta_task.start()
    fab_task.start()


if __name__ == "__main__":
    connector(curr_data)
