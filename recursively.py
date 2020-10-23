import requests
import re
from bs4 import BeautifulSoup
file = open('./data/giant.txt', 'a')


def is_good(tag):
    if (
            tag.name != 'a'
            or 'href' not in tag.attrs
            or not tag.attrs['href'].startswith('/wiki/')
            or ('title' in tag.attrs and ':' in tag.attrs['title'])
            or tag.text == 'англ.'
    ):
        return False
    return True


def recursively_parse(current, parent='None', depth=5):
    if depth == 0:
        return

    r = requests.get(current, stream=True)
    if r.status_code != 200:
        print('Error:', current)
        return

    content = BeautifulSoup(r.content, 'html.parser').findChild("div", {'id': 'content'})
    title = content.find('h1').text
    if ':' in title or re.match('[\S|\s]*\d[\S|\s]*', title):
        return
    file.write('{} *** {} *** {} \n'.format(title, parent, current))
    print('Title', depth, title)

    for tag in content.find_all():
        if tag.text == 'Литература' or tag.text == 'Примечания':
            return
        if is_good(tag):
            recursively_parse('https://ru.wikipedia.org{}'.format(tag.attrs['href']), current, depth - 1)
