
from faker import Faker
from urllib.parse import urlparse

fake_fr = Faker('fr_FR')
def generate_random_header(url):

    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    machine = {
        'User-Agent': fake_fr.user_agent(),
        'Referer': url,
        'X-Forwarded-For': fake_fr.ipv4_public(),
        'X-Requested-With': fake_fr.random_element(elements=['XMLHttpRequest', 'Fetch']),
        # 'Authorization': fake_fr.password(length=20, special_chars=True, digits=True, upper_case=True, lower_case=True),
        'Origin': base_url,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    return machine



