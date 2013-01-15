from bs4 import BeautifulSoup as BS
import requests as r

def get_ids_from_page(page):
    response = r.get(page)
    soup = BS(response.content).body

    return sorted([x.get('id') for x in soup.find_all() if x.get('id') is not None])

if __name__ == '__main__':
    # In response to the question at the URL below - in short "How do I get the
    #   ids from all objects on a page in Python?"
    ids = get_ids_from_page('http://stackoverflow.com/questions/14347086/')

    for val in ids:
        print val