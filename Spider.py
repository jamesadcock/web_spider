#Takes a URL and spider the site and downloads all of the pages

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse

#Starts the spider running
def start_spider():
    base_url = input('Please enter the base URL: ')
    hyperlinks = list()
    hyperlinks.append(base_url)
    index = 0
    while True:
        hyperlinks[index] = convert_to_absolute_path(hyperlinks[index], base_url)
        html = get_page_html(hyperlinks[index])
        url = urlparse(hyperlinks[index])
        hyperlinks = hyperlinks + find_hyper_links(html)
        hyperlinks = remove_duplicates(hyperlinks)
        file_name = str(url.path + url.query)
        file_name = file_name.replace('/', '_')
        if file_name:
            write_to_file(get_page_html(hyperlinks[index]), file_name, 'html')
        if len(hyperlinks) - 1 == index:
            break
        index += 1

#Takes a a url and returns the page html
def get_page_html(url):
    code = requests.get(url)
    html = code.text
    return html

#Takes a text, file name and the file extension and writes the text to a file with the specified and and extension
def write_to_file(text, file_name, ext):
    file_writer = open(file_name + '.' + ext, 'w', encoding='utf-8')
    file_writer.write(text)
    file_writer.close()
    print('Created ' + file_name + '.' + ext)

#takes html as an argument and returns a set of all the href values of any anchor tags
def find_hyper_links(html):
    formatted_html = BeautifulSoup(html)
    hyper_links = list()
    for link in formatted_html.findAll('a'):
        match = re.search(r'^http|^/', link.get('href'))
        if match:
            hyper_links.append(link.get('href'))
    return hyper_links

#If a relative path is passed in as an argument it the absolute path.  If a absolute path is passed in as an
#argument it simply returns the absolute path
def convert_to_absolute_path(link, base_url):
    match = re.search(r'^http', link)
    if match:
        return link
    else:
        url = urlparse(base_url)
        link = link.replace('/', '')
        link = url.scheme + '://' + url.hostname + '/' + link + url.query
        print(link)
        return link

# takes a list as an argument, strips out any duplicate values and returns the list (not very fast)
def remove_duplicates(item_list):
    unique_list = []
    [unique_list.append(i) for i in item_list if not unique_list.count(i)]
    return unique_list

start_spider()
