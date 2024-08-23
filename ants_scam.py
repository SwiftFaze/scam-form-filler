import requests
import threading
import time
import random
import string
from lib.user_info_lib import generate_random_person


def generate_random_string(length):
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_multipart_body(form_data, boundary):
    lines = []
    for name, value in form_data.items():
        lines.append(f'--{boundary}')
        lines.append(f'Content-Disposition: form-data; name="{name}"')
        lines.append('')
        lines.append(value)
    lines.append(f'--{boundary}--')
    lines.append('')
    body = '\r\n'.join(lines)
    return body




with open('url_lists/ants_scam_url_list.txt', 'r') as file:
    urls = file.read().splitlines()


headers = {
    'Content-Type': 'multipart/form-data; boundary=<calculated when request is sent>',
    'User-Agent': 'PostmanRuntime/7.29.0',
    'Accept': '*/*',
    'Cache-Control': 'no-cache',
    'Accept-Encoding': 'gzip, deflate, br',
    'Host': '<calculated when request is sent>',
    'Content-Type': '<calculated when request is sent>',
    'Content-Length': '<calculated when request is sent>',
    'Cookie': 'user_session=01c488ae13654584e5241d4b09fb650c7633b; PHPSESSID=21gscu34houkprv9l3154bft7q89r',
}



success_counter = 0
counter_lock = threading.Lock()

def send_post_request():
    global success_counter
    while True:
        try:
            time.sleep(random.randint(1, 2))
            for url in urls:
                
                person = generate_random_person()
                form_data = {
                    'nom': person['full_name'], 
                    'cb': person['bank_card_number'], 
                    'date': person['bank_card_expiration'], 
                    'cvv': person['bank_card_cvv'], 
                }
                print(form_data)

                # Generate boundary, Content-Type, and Content-Length
                boundary = '----WebKitFormBoundary' + generate_random_string(16)
                body = generate_multipart_body(form_data, boundary)
                content_length = str(len(body))
                content_type = f'multipart/form-data; boundary={boundary}'
                host = url.split('/')[2]  # Extract the host from the URL


                # Set the headers
                headers = {
                    'Content-Type': content_type,
                    'Content-Length': content_length,
                    'User-Agent': 'PostmanRuntime/7.29.0',
                    'Accept': '*/*',
                    'Cache-Control': 'no-cache',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Host': host,
                    'Cookie': 'user_session=01c488ae13654584e5241d4b09fb650c7633b; PHPSESSID=21gscu34houkprv9l3154bft7q89r',
                }


                print(headers)
                response = requests.post(url, data=form_data, headers=headers, timeout=5)

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
        

num_threads = 1
threads = []

for i in range(num_threads):
    thread = threading.Thread(target=send_post_request)
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print(f'Total successful requests: {success_counter}')
