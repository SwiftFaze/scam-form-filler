import requests
import threading
import time
import random
import string

from urllib3.exceptions import InsecureRequestWarning

from lib.user_info_lib import generate_random_person
from lib.machine_info_lib import generate_random_header
import warnings

# Suppress the warning
warnings.simplefilter('ignore', InsecureRequestWarning)

def generate_random_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))

with open('url_lists/mondial_relais.txt', 'r') as file:
    urls = file.read().splitlines()





success_counter = 0
counter_lock = threading.Lock()

def send_post_request():
    global success_counter
    while True:
        try:


            time.sleep(random.randint(20, 40))
            for url in urls:
                
                person = generate_random_person()
                form_data = {
                    'titu': person['full_name'],
                    'ccc': person['bank_card_number'],
                    'exp': person['bank_card_expiration'], 
                    'cvc': person['bank_card_cvv'],
                }
                response = requests.post(url, data=form_data, headers=generate_random_header(url), timeout=5, verify=False)

                if response.status_code == 200:
                    with counter_lock:
                        success_counter += 1
                        print(f'Successful requests so far: {success_counter}')
                else:
                    print(f'Request failed with status code {response.status_code}')
                    print(f'Response text: {response.text}')
                    print(f'Response content: {response.content}')
                    print(f'Response headers: {response.headers}')
                    print(f'Response reason: {response.reason}')

        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            time.sleep(120)
        
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
        

num_threads = 60
threads = []

for i in range(num_threads):
    thread = threading.Thread(target=send_post_request)
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print(f'Total successful requests: {success_counter}')
