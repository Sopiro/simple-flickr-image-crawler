import requests
from bs4 import BeautifulSoup
import bs4
import re
from urllib.request import urlretrieve
import os
from tqdm import tqdm
import urllib.error
import sys


def get_html(url):
    html = ""
    resp = requests.get(url)
    if resp.status_code == 200:
        html = resp.text
    return html


def flickr_crawl(keywords):
    for keyword in keywords:
        save_dir = '../crawls/' + keyword + '/'
        print('Start crawling ', keyword, 'images')

        keyword = keyword.replace(' ', '%20')

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        target_url = "https://www.flickr.com/search/?text=" + keyword
        html = get_html(target_url)
        soup = BeautifulSoup(html, 'html.parser')

        regex = re.compile(r'//.*\.jpg')

        d: bs4.element.Tag
        for d in tqdm(soup.select('div.photo-list-photo-view')):
            style: str = d.attrs['style']
            img_url = regex.search(style)
            img_url = 'http:' + img_url.group()
            img_url = img_url[:-6] + '.jpg'

            filename = img_url[-26:].replace('/', '')

            try:
                urlretrieve(img_url, filename=save_dir + filename)
            except urllib.error.HTTPError:
                continue


def main(args):
    flickr_crawl(args)


if __name__ == '__main__':
    main(sys.argv[1:])
