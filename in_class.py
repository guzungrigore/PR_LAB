import requests
from bs4 import BeautifulSoup
import re

prefix = 'https://999.md'
base_url = 'https://999.md/ru/list/real-estate/apartments-and-rooms'


def parse(local_url):
    response = requests.get(local_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = set()
        pattern = r'^/ro/\d{8}$'
        for link in soup.find_all('a', href=re.compile(pattern)):
            href = link.get('href')
            links.add(prefix + href)

        return links


def recurse_pages(max_pages):
    result = set()
    for page in range(1, max_pages + 1):
        page_url = f"{base_url}?page={page}"
        result.update(parse(page_url))
    return result


max_pages = 10
links = recurse_pages(max_pages)
for link in links:
    print(link)
