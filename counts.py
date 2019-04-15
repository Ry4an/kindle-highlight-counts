from __future__ import print_function
import ConfigParser
from goodreads import client
from bs4 import BeautifulSoup
import sys
import csv

# Downloaded HTML for https://www.goodreads.com/notes/28705542-ry4an
EXAMPLE_NOTES_HTML_FILE = "annotatedBookItem__knhLink.html"

def get_notes_urls(filename):
    with open(filename) as html_fp:
        soup = BeautifulSoup(html_fp, 'html.parser')
    tags = soup.find_all('a', class_="annotatedBookItem__knhLink")
    return [ tag.get('href') for tag in tags ]

def get_api_creds():
    # return api_key, api_secret tuple
    config = ConfigParser.RawConfigParser()
    config.read('api-key.ini')
    return (config.get('developer', 'key'), config.get('developer', 'secret'))

def url_to_book_dict(url, gc):
    # take a notes URL and a good reads client and get the book object's dict
    # ex: https://www.goodreads.com/notes/40192833-new-york-2140/28705542-ry4an?ref=abp
    PREFIX = "https://www.goodreads.com/notes/"
    book_num = int(url[len(PREFIX):].split("-")[0])
    book_dict = gc.book(book_num)._book_dict
    book_dict['highlight_url'] = url
    book_dict['book_num'] = book_num
    return book_dict

def main():

    gc = client.GoodreadsClient(*get_api_creds())

    MAX = None  # set to 1 for faster debugging

    books = [url_to_book_dict(url, gc) for url in get_notes_urls(EXAMPLE_NOTES_HTML_FILE)[0:MAX]]

    FIELDS = "title book_num num_pages average_rating link highlight_url ratings_count rating_dist".split()
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(books)

if __name__ == "__main__":
    main()
