# Main script 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import os
import traceback
import requests 
from dotenv import load_dotenv

load_dotenv()

#処理が完了したらLINEに通知する
def post_line(message):
    url = "https://notify-api.line.me/api/notify"
    token = os.environ['LINE_NOTIFY_TOKEN']
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}
    post = requests.post(url ,headers = headers ,params=payload)
    
#秒数をランダムに生成して、その秒数だけ待つ
def wait_random_seconds():
    return random.randint(1, 300)

def login_to_chatwork(driver, username, password):
    driver.get("https://www.chatwork.com/login.php")
    time.sleep(2)
    
    username_field = driver.find_element(By.ID, "username")
    username_field.send_keys(username)
    time.sleep(2)
    
    #エンターキーを押す
    username_field.send_keys(Keys.RETURN)
    time.sleep(2)
    
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys(password)
    time.sleep(2)
    #エンターキーを押す
    password_field.send_keys(Keys.RETURN)
    time.sleep(2)
    

def send_message(driver, room_id, message):
    room_url = os.getenv("CHATWORK_ROOM_URL")
    
    driver.get(f"https://www.chatwork.com/#!rid{room_id}")
    time.sleep(3)
    #暗黙的に待つ
    driver.implicitly_wait(10)
    
    message_field = driver.find_element(By.XPATH, '//*[@id="_chatText"]')
    message_field.send_keys(message)
    
    #command + enterkeyを押す
    message_field.send_keys(Keys.COMMAND + Keys.RETURN)
    time.sleep(2)
    
    
def main():
    #変数は.envファイルに保存しておく
    username = os.getenv("CHATWORK_USERNAME")
    password = os.getenv("CHATWORK_PASSWORD")
    room_id = os.getenv("CHATWORK_ROOM_ID")

    messages = [
        "おはようございます。業務を開始します。",
        "おはようございます。業務を開始します！",
        "おはようございます。本日の業務を開始します。",
        "おはようございます！業務を開始します。",
        "おはようございます。業務を開始いたします。",
        "おはようございます！業務を開始します！"
    ]
    
    message = random.choice(messages)

    try:
        wait_random_second:int = wait_random_seconds()
        post_line('chatworkの投稿処理を開始しました。今日は' + str(round((wait_random_second/60), 2)) + '分待ちます。')
        print('chatworkの投稿処理を開始しました。今日は' + str(round((wait_random_second/60), 2)) + '分待ちます。')
        time.sleep(wait_random_second)
        driver = webdriver.Chrome()# ChromeDriverのパスを指定する場合は、引数にパスを渡す
        login_to_chatwork(driver, username, password)
        send_message(driver, room_id, message)
        post_line('chatworkの投稿処理が完了しました。')
    except Exception as e:
        error_message = traceback.format_exc()
        print(error_message)
        post_line(f'chatworkの投稿処理がエラーになりました。{error_message}')
        time.sleep(10)  
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
