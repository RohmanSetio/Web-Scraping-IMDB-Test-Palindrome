import requests 
import mysql.connector
from pyquery import PyQuery


def get_url(url, headers):
    response = requests.get(url, headers=headers)
    html = PyQuery(response.text)
    
    urls = []
    for a in html.find('div[class="sc-3450242-3 fLFQmt ipc-page-grid__item ipc-page-grid__item--span-2"] ul li a'):
        urls.append(PyQuery(a).attr('href'))
    
    return urls

def save_database(data):
    config = {
        'user': 'root',
        'password': '1234',
        'host': 'localhost',
        'database': 'imdb_data'
    }
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    sql = 'INSERT IGNORE INTO nama_movie(title, year, rating) VALUES (%s, %s, %s)'
    cursor.execute(sql, (
        data["Title"], data["Year"], data["Rating"]
    ))

    conn.commit()
    conn.close()

def extract(web_url, headers):
    try:
        response = requests.get(web_url, headers=headers)
        html = PyQuery(response.text)
        result = {
            "Title": html.find('div[class="sc-69e49b85-0 jqlHBQ"] h1').text(),
            "Year": html.find('li[data-testid="title-details-releasedate"] div ul li a').text().split(" ")[2],
            "Rating": html.find('div[class="sc-bde20123-2 cdQqzc"] span[class="sc-bde20123-1 cMEQkK"]').text().split(" ")[0]
        }
        
        save_database(result)

    except Exception as exc:
        print(f'data tidak dari {web_url}: {str(exc)}')

def execute():
    base_url = 'https://m.imdb.com/'
    main_url = 'https://m.imdb.com/chart/top/?ref_=nv_mv_250'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    }
    web_url = 0
    while True:
        urls = get_url(main_url, headers)
        for url in urls:
            extract(base_url + url, headers)
            web_url += 1
            if web_url == 200:
                return

execute()
