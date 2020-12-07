from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import multiprocessing
import mysql.connector as ms
import pickle


def tasko(usero):
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(
        executable_path="chromedriver.exe", options=chrome_options
    )
    driver.get("https://instagram.com")
    # pickle.dump(driver.get_cookies(), open("insta.pkl", "wb"))
    cookies = pickle.load(open("insta.pkl", "rb"))

    for cookie in cookies:
        driver.add_cookie(cookie)
    for user in usero:
        driver.get(f"https://instagram.com/{user}")
        try:
            element = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Follow"]'))
            )
            element.click()
        except:
            pass


def connector():
    while True:
        db = ms.connect(
            host="logs.c7xtjtjv8ph3.ap-south-1.rds.amazonaws.com",
            port=3306,
            user="shubh",
            passwd="shubh2003",
            db="tasker",
        )
        cursor = db.cursor()
        cursor.execute("select insta from users;")
        b = cursor.fetchall()
        users = [i[0] for i in b]
        # print(users)
        with open("insta_users.txt", "r+") as f:
            curr_users = f.readlines()
            curr_users = [i.replace("\n", "") for i in curr_users]
        new_users = [i for i in users if i not in curr_users]
        if len(new_users) == 0:
            pass
        else:
            print("FOLLOWING THE FOLLOWING ACCOUNT xD:")
            print(new_users)
            with open("insta_users.txt", "a+") as f:
                for i in new_users:
                    f.write(i)
                    f.write("\n")
            taske = multiprocessing.Process(target=tasko, args=(new_users,))
            taske.daemon = True
            taske.start()
            new_users.clear()
            continue


if __name__ == "__main__":
    connector()