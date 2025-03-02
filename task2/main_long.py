import requests
from bs4 import BeautifulSoup

url = 'https://quotes.toscrape.com'

url_for_links = url

def some_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "No more page."
        except IndexError:
            return "IE"
        except UnboundLocalError:
            return "ULE"
        except AttributeError:
            return "AE"
    return inner

def swap_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    next_page = soup.find('li', class_='next')
    if next_page:
        next_page = next_page.a['href']
        url = 'https://quotes.toscrape.com'+next_page
        next_page = None
        return url
    else:
        return None

@some_error
def  get_authors(url):
    if url:
        list = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        authors  = soup.find_all('small', class_='author')
        for object in authors:
            list.append(object.text)
        return list

@some_error
def  get_quotes(url):
    if url:
        list = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        qoutes = soup.find_all('span', class_='text')
        for object in qoutes:
            list.append(object.text)
        return list

@some_error
def  get_tags(url):
    if url:
        list = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        tag_div = soup.find_all('div', class_='tags')
        for object in tag_div:
            tags = object.find_all('a', class_='tag')
            tags_list = []
            for object in tags:
                tags_list.append(object.text)
            list.append(tags_list)
        return list

@some_error
def make_qoutes(tags,author,quote):
    qoutes = []
    for i in range(len(author)):
        object = {}
        object['tags'] = tags[i]
        object['author'] = author[i]
        object['quote'] = quote[i]
        qoutes.append(object)
    return qoutes

@some_error
def  get_links(url):
    if url:
        list = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.find_all('a', href=True)
        for object in links:
            if '/author/' in object['href']:
                list.append(url_for_links+object['href'])
        return list

@some_error
def  get_fullname(url):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        object  = soup.find('h3', class_='author-title')
        return object.text

@some_error
def  get_borndate(url):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        object  = soup.find('span', class_='author-born-date')
        return object.text

@some_error
def  get_bornlocation(url):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        object  = soup.find('span', class_='author-born-location')
        return object.text
    
@some_error
def  get_description(url):
    if url:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        object  = soup.find('div', class_='author-description')
        return object.text.strip()
    
@some_error
def make_author(fullname,borndate,bornlocation,description):
    object = {}
    object['fullname'] = fullname
    object['born_date'] = borndate
    object['born_location'] = bornlocation
    object['description'] = description
    return object
    
@some_error
def main(url):
    links = []
    quotes = []
    authors = []
    while True:
        if url:
            links.extend(get_links(url))
            quotes.extend(make_qoutes(get_tags(url),get_authors(url),get_quotes(url)))
            url = swap_page(url)
        else:
            for url in links:
                authors.append(make_author(get_fullname(url),get_borndate(url),get_bornlocation(url),get_description(url)))
            print(authors)
            break

if __name__ == "__main__":
    main(url)




# for author in authors:
#     print(f"1.{author.name}\n2.{author.attrs}\n3.{author.contents}\n4.{author.children}\n5.{author.parent}\n")