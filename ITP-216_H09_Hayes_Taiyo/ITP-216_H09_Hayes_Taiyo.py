# Taiyo Hayes, tjhayes@usc.edu
# ITP 216, Fall 2022
# Section: 32081
# Homework 9
# Description: Parse music venue websites

import ssl
from urllib.parse import urljoin
import urllib.request
import os

from bs4 import BeautifulSoup as bs

def retrieve_and_store_webpage(url, ctx, fn):
    page = urllib.request.urlopen(url, context=ctx)
    soup = bs(page.read().decode('utf-8'), 'html.parser')
    f = open(fn, 'w', encoding='utf-8')
    print(soup, file=f)
    f.close()


def load_webpage(url, ctx):
    page = urllib.request.urlopen(url, context=ctx)
    return bs(page.read(), 'html.parser')


def relative_file_path_to_URL(relative_file_path):
    # expand relative to absolute
    absolute_file_path = os.path.abspath(relative_file_path)
    # prepend file:// on UNIX-style OSes like Mac and Linux and file:/// on Windows
    file_name_url = urljoin('file:', urllib.request.pathname2url(absolute_file_path))
    return file_name_url


def main():
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # url1 = 'https://www.thenovodtla.com/events'
    # url2 = 'https://www.livenation.com/venue/KovZpZAEAl6A/the-wiltern-events'

    # retrieve_and_store_webpage(url1, ctx, 'novo.html')
    # retrieve_and_store_webpage(url2, ctx, 'wiltern.html')

    relative_file_path1 = 'sites/novo.html'
    file_name_url1 = (relative_file_path_to_URL(relative_file_path1))

    relative_file_path2 = 'sites/wiltern.html'
    file_name_url2 = (relative_file_path_to_URL(relative_file_path2))

    soup1 = load_webpage(file_name_url1, ctx)  # load webpage from local file
    soup2 = load_webpage(file_name_url2, ctx)

    info_wraps1 = soup1.find_all('div', class_='info')
    info_wraps2 = soup2.find_all('div', class_='listing__item__details')
    print("Concerts coming up at Novo:")
    for info in info_wraps1:
        print("\t" + info.span.text.strip())
        print("\t\t"+ info.h3.text.strip())

    print("\nConcerts coming up at The Wiltern:")
    for info in info_wraps2:
        print("\t" + info.time.text)
        print("\t\t" + info.h3.text)


if __name__ == '__main__':
    main()