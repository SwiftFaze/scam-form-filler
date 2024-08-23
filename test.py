import requests

# URL to send the GET request to
url = "https://bvb.qfv.mybluehost.me/manager/amendes.org/amendes.org/"

# Define custom headers
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-US,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Priority': 'u=0, i',  # Note: This header might not be recognized by all servers
    'Sec-CH-UA': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
    'Sec-CH-UA-Mobile': '?0',
    'Sec-CH-UA-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Sec-GPC': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
}

# Send the GET request with custom headers
response = requests.get(url, headers=headers)

# Output the response status and headers
print(f"Status Code: {response.status_code}")
print(f"Headers: {response.headers}")

# Check if 'PHPSESSID' is in the cookies
phpsessid = response.cookies.get('PHPSESSID')

if phpsessid:
    print(f"PHPSESSID: {phpsessid}")
else:
    print("PHPSESSID not found in the response.")
