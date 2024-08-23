import requests
import threading
import time
import random
import string
from lib.user_info_lib import generate_random_person


def generate_random_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))

with open('url_lists/impots_scam_url_list.txt', 'r') as file:
    urls = file.read().splitlines()


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'PostmanRuntime/7.29.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


success_counter = 0
counter_lock = threading.Lock()

def send_post_request():
    global success_counter
    while True:
        try:
            time.sleep(random.randint(1, 20))
            for url in urls:
                
                person = generate_random_person()
                form_data = {
                    'prenom': person['first_name'], 
                    'nom': person['last_name'], 
                    'j': person['dob_day'], 
                    'mo': person['dob_month'], 
                    'an': person['dob_year'], 
                    'adresse': person['address'], 
                    'cp': person['postal_code'], 
                    'tel': person['telephone'], 
                    'cb': person['bank_card_number'], 
                    'm': person['bank_card_month'], 
                    'a': person['bank_card_year'], 
                    'cvv': person['bank_card_cvv'], 
                }


                response = requests.post(url, data=form_data, headers=headers, timeout=5)

                if response.status_code == 200:
                    with counter_lock:
                        success_counter += 1
                        print(f'Successful requests so far: {success_counter}')
                else:
                    print(f'Request failed with status code {response.status_code}')

        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            time.sleep(20)
        
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
