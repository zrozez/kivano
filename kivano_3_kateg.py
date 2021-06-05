import requests
from bs4 import BeautifulSoup
import pandas as pd

class Writer:
    def __init__(self, tovary):
        self.depDF = pd.DataFrame(
            {'names': tovary.names,
            'links': tovary.links,
            'names_of_categories': tovary.names_of_categories
            }
        )

    def write_to_csv(self):
        csvFileContents = self.depDF.to_csv(index=False)
        with open("tovary.csv", "w", encoding='utf-8') as f:
            f.write(csvFileContents)


class Tovary:
    def __init__(self, tovars):
        self.tovars = tovars

        self.names = []
        self.links = []
        self.names_of_categories = []

        for tovar in self.tovars:
            self.names.append(tovar.name)
            self.links.append(tovar.link)
            self.names_of_categories.append(tovar.name_of_category)

class Tovar:
    def __init__(self, name, link, name_of_category):
        self.name = name
        self.link = link
        self.name_of_category = name_of_category

class Find_tovars:
    def __init__(self, url):
        self.url = url
        self.resp = requests.get(self.url).text
        self.soup = BeautifulSoup(self.resp, 'html.parser')

    def total_pages(self):
        pages = self.soup.find('div', class_ = 'pager-wrap').find_all('a')[-1].get('href')
        last_page = pages.split('=')[-1]
        return int(last_page)

    def info(self, lst):
        ads = self.soup.find('div', class_ = 'list-view').find_all('div', class_ = 'item')
        ads2 = self.soup.find('div', class_ = 'product-index')
        self.url = 'https://www.kivano.kg'
        name_of_category = ads2.find('h1', class_ ='page-title').text
        for ad in ads:
            try:
                name = ad.find('div', class_ = 'listbox_title').text.replace('\n', '')
            except:
                name = 'Нет имени товара'
            try:
                link = ad.find('div', class_ = 'listbox_title').find('a').get('href')
                link = self.url+link
            except:
                link = 'Нет ссылки на товар'
            lst.append(Tovar(name, link, name_of_category))
        return lst

def itog(url):
    tovars = []
    part_of_page = '?page='
    tovar_ = Find_tovars(url)
    total_page = tovar_.total_pages()
    for i in range(1, total_page+1):
        urls = url + part_of_page + str(i)
        tovar_.info(tovars)
    return tovars

def add_to_lst(first_lst, tov):
    for i in tov:
        first_lst.append(i)
    return first_lst

parfumeriya = 'https://www.kivano.kg/parfyumeriya'
igrushki = 'https://www.kivano.kg/igrushki'
umnyi_dom = 'https://www.kivano.kg/umnyy-dom-i-bezopasnost'
sport = 'https://www.kivano.kg/trenazhery'

parfume = itog(parfumeriya)
igru = itog(igrushki)
lst = add_to_lst(parfume, igru)

smart_home = itog(umnyi_dom)
lst = add_to_lst(lst, smart_home)

trenya = itog(sport)
lst = add_to_lst(lst, trenya)
t = Tovary(lst)
w = Writer(t)
w.write_to_csv()
