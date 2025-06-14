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
    referCode = 'ot2n'
    global start
    while True:
        try:
            time.sleep(random.randint(1, 2))
            start = time.time()
            for url in urls:

                password = generate_random_string(6)
                hash = hashlib.md5(password.encode()).hexdigest()

                person = generate_random_person()
                email = person['email']


                form_data = {
                    'captcha': generate_random_string(9999),
                    'memberName': email,
                    'password': hash,
                    'referrerAccount': referCode,
                }

                response = requests.post(url, json=form_data, timeout=5)


                if response.status_code == 200:

                    with counter_lock:
                        form_data = {
                            'grant_type': 'mobile_password',
                            'username': email,
                            'tenantId': '000000',
                            'password': hash,
                            'scope': 'all',
                        }

                        headers = {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Accept': 'application/json, text/plain, */*',
                            'Authorization': 'Basic Z2FtZTpnYW1lX3NlY3JldA==',
                            'Tenant-Id': '000000',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                            'Origin': 'https://crypto-webs.bond',
                            'Referer': 'https://crypto-webs.bond/',
                        }

                        response = requests.post(login_url, data=form_data, headers=headers)
                        if response.status_code == 200:
                            # Parse response as JSON
                            login_data = response.json()

                            # Extract token and userId (you may need to adjust keys)
                            token = login_data.get("access_token")
                            memberId = login_data.get("user_id") or login_data.get("user", {}).get("user_id")  # fallback

                            if token and memberId:
                                login_data = response.json()

                                # Get the Blade token and user ID
                                blade_token = login_data.get("access_token")
                                member_id = login_data.get("user_id")

                                if not blade_token or not member_id:
                                    print("Missing token or user ID.")
                                    return

                                # Construct headers for the next request
                                auth_headers = {
                                    'Authorization': 'Basic Z2FtZTpnYW1lX3NlY3JldA==',
                                    'Blade-Auth': blade_token,
                                    'Content-Type': 'application/x-www-form-urlencoded',
                                    'Accept': 'application/json, text/plain, */*',
                                    'User-Agent': 'Mozilla/5.0',
                                }

                                # Build the GET URL (can be POST too — looks like GET in your example)
                                member_url = f'https://crypto-webs.bond/api/trading/memberclient/getMember?memberId={member_id}'

                                # Make the request
                                response = requests.get(member_url, headers=auth_headers)

                                if response.status_code == 200:


                                    auth_headers = {
                                        'Authorization': 'Basic Z2FtZTpnYW1lX3NlY3JldA==',
                                        'Blade-Auth': blade_token,
                                        'Content-Type': 'application/json',   # <- set to application/json here
                                        'Accept': 'application/json, text/plain, */*',
                                        'User-Agent': 'Mozilla/5.0',
                                    }
                                    form_data = {
                                        'ifscCode': '',
                                        'memberId': memberId,
                                        'payBank': person['bank_name'],
                                        'payName': person['full_name'],
                                        'payNumber': person['iban'],
                                        'payRut': '',
                                        'payType': '',
                                        'playerAccount': email,
                                    }

                                    bank_url = f'https://crypto-webs.bond/api/trading/memberclient/addBankInfo'
                                    response = requests.post(bank_url, json=form_data, headers=auth_headers)

                                    if response.status_code == 200:

                                        auth_headers = {
                                            'Authorization': 'Basic Z2FtZTpnYW1lX3NlY3JldA==',
                                            'Blade-Auth': blade_token,
                                            'Content-Type': 'application/json',   # <- set to application/json here
                                            'Accept': 'application/json, text/plain, */*',
                                            'User-Agent': 'Mozilla/5.0',
                                        }

                                        refer_url = f'https://crypto-webs.bond/api/trading/memberclient/getMember?memberId={member_id}'
                                        response = requests.get(refer_url, headers=auth_headers)

                                        if response.status_code == 200:
                                            success_counter += 1

                                            print(f'[{time.time() - start:.2f}s] : {success_counter} - email: {email} - password: {password} - referer code: {referCode}')
                                            data = response.json().get("data", {})
                                            new_refer_code = data.get("referCode")
                                            referCode = new_refer_code



                                        else:
                                            print(f'Request failed step 1 {response.status_code}')
                                            print(f'Response text: {response.text}')
                                            print(f'Response content: {response.content}')
                                            print(f'Response headers: {response.headers}')
                                            print(f'Response reason: {response.reason}')


                                    else:
                                        print(f'Request failed step 2 {response.status_code}')
                                        print(f'Response text: {response.text}')
                                        print(f'Response content: {response.content}')
                                        print(f'Response headers: {response.headers}')
                                        print(f'Response reason: {response.reason}')

                                else:
                                    print("Failed to fetch member info")
                                    print("Status:", response.status_code)
                                    print("Response:", response.text)

                            else:
                                print("Login succeeded but token or memberId missing")



                        else:
                            print(f'Request step 3 {response.status_code}')
                            print(f'Response text: {response.text}')
                            print(f'Response content: {response.content}')
                            print(f'Response headers: {response.headers}')
                            print(f'Response reason: {response.reason}')



                else:
                    # print(f'RBAD REFER CODE {referCode}')
                    referCode = 'h685'
                    # print(f'Request failed step 4{response.status_code}')
                    # print(f'Response text: {response.text}')
                    # print(f'Response content: {response.content}')
                    # print(f'Response headers: {response.headers}')
                    # print(f'Response reason: {response.reason}')

        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            time.sleep(120)

        except requests.exceptions.RequestException as e:
            print(f'Request failed: {e}')


num_threads = 3
threads = []

for i in range(num_threads):
    thread = threading.Thread(target=send_post_request)
    thread.start()
    threads.append(thread)


for thread in threads:
    thread.join()

print(f'Total successful requests: {success_counter}')
