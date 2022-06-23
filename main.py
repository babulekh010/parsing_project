import requests
from bs4 import BeautifulSoup
import csv

def get_html(url):
    response = requests.get(url)
    return response.text

def get_data_from_html(html):
    soup = BeautifulSoup(html, 'lxml')
    products_list = soup.find("div", "table-view-list")
    products = products_list.find_all("div", class_="list-item")
    for product in products:
        try:
            title = product.find('h2', class_='name').text.strip()
        except:
            title = ''
        try:
            year = product.find('p', class_='year-miles').find('span').text.strip()
            color = product.find('p', class_='year-miles').find('i', class_='color-icon').get('title').strip()
            body_type = product.find('p', class_='body-type').text.strip()
            desc = f"{year},{body_type} {color}"
        except:
            desc = ''
        try:
            price = product.find('p', class_='price').find('strong').text
        except:
            price = ''
        try:
            image = product.find('div', class_='thumb-item-carousel').find('img').get('data-src')
        except:
            image = ''
        data = {'title': title, 'desc': desc, 'price': price, 'image': image}
        write_to_csv(data)

def write_to_csv(data):
    with open('cars.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow((data['title'], data['desc'], data['price'], data['image']))

def get_last_page(html):
    soup = BeautifulSoup(html, 'lxml')
    last_page = soup.find('ul', class_='pagination').find_all('a')[-4].text
    return int(last_page)

def main():
    url = "https://www.mashina.kg/motosearch/all/?type=20"
    pages = '&page='
    last_page = get_last_page(get_html(url))
    for page in range(1, last_page):
        new_url = url + pages + str(page)
        get_data_from_html(get_html(new_url))
main()
