import requests
import threading
import time
import random
import string

def generate_random_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))

url = 'https://emailmarketing.locaweb.com.br/accounts/192883/messages/3/clicks/113679/2?envelope_id='
max_envelope_counter = 2000


headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'PostmanRuntime/7.29.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}


success_counter = 0
envelope_counter = 0

counter_lock = threading.Lock()

def send_post_request():
    global success_counter
    global envelope_counter
    while True:
        try:
                if envelope_counter < max_envelope_counter:

                    response = requests.get(url+str(envelope_counter), headers=headers, timeout=5)
                    if response.status_code == 200:
                        with counter_lock:
                            success_counter += 1
                            envelope_counter += 1
                            print(f'Successful requests so far: {success_counter} - envelope_id: {envelope_counter}')
                    else:
                        print(f'Request failed with status code {response.status_code}')
                        print(f'Response text: {response.text}')
                        print(f'Response content: {response.content}')
                        print(f'Response headers: {response.headers}')
                        print(f'Response reason: {response.reason}')
                else:
                    envelope_counter = 0
        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            time.sleep(120)
        
        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')
        

num_threads = 100
threads = []

for i in range(num_threads):
    thread = threading.Thread(target=send_post_request)
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print(f'Total successful requests: {success_counter}')
