import json
import requests
from tools import check_database, stop_message, start_message
from config import key, categoryId, locationId, searchRadius, priceMin, priceMax, sort, withImagesOnly, limit_page, \
    cookie, owner, display, search
import sys
from datetime import datetime
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager
from urllib3.util import ssl_
import re

start_message()

CIPHERS = """ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-SHA384:ECDHE-ECDSA-AES256-SHA384:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-SHA256:AES256-SHA"""


class TlsAdapter(HTTPAdapter):
    def __init__(self, ssl_options=0, **kwargs):
        self.ssl_options = ssl_options
        super(TlsAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, *pool_args, **pool_kwargs):
        ctx = ssl_.create_urllib3_context(ciphers=CIPHERS, cert_reqs=ssl.CERT_REQUIRED, options=self.ssl_options)
        self.poolmanager = PoolManager(*pool_args, ssl_context=ctx, **pool_kwargs)


def except_error():  # Эту функцию можно дополнить, например обработку капчи
    sys.exit(1)
s = requests.Session()                          # Будем всё делать в рамках одной сессии
proxiess = {'http': '185.170.215.228:80'}
proxiess = {'http': '79.143.225.152:60517'}
s = requests.session()
adapter = TlsAdapter(ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1)
s.mount("https://", adapter)
headers = {'Host': 'm.avito.ru',
           'pragma': 'no-cache',
           'cache-control': 'no-cache',
           'upgrade-insecure-requests': '1',
           'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
           'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'sec-fetch-site': 'none',
           'sec-fetch-mode': 'navigate',
           'sec-fetch-user': '?1',
           'sec-fetch-dest': 'document',
           'accept-language': 'ru-RU,ru;q=0.9', }
if cookie:  # Добавим куки, если есть внешние куки
    headers['cookie'] = cookie
s.headers.update(headers)  # Сохраняем заголовки в сессию
s.get('https://m.avito.ru/',
      proxies=proxiess)  # , useragent = UA) #   useragent = str(UA)                 # Делаем запрос на мобильную версию.
url_api_9 = 'https://m.avito.ru/api/9/items'  # Урл первого API, позволяет получить id и url объявлений по заданным фильтрам
params = {
    'key': key,
    'categoryId': categoryId,
    'locationId': locationId,
    'searchRadius': searchRadius,
    'priceMin': priceMin,
    'priceMax': priceMax,
    'owner': owner,
    'sort': sort,
    'withImagesOnly': withImagesOnly,
    'display': display,
    'limit': limit_page,
    'query': search,
}
cicle_stop = True  # Переменная для остановки цикла
cicle = 0  # Переменная для перебора страниц с объявлениями
items = []  # Список, куда складываем объявления
while cicle_stop:
    cicle += 1  # Так как страницы начинаются с 1, то сразу же итерируем
    params['page'] = cicle
    res = s.get(url_api_9, params=params, proxies=proxiess)  # , useragent = UA) #, useragent = str(UA))
    try:
        res = res.json()
    except json.decoder.JSONDecodeError:  # {'code': 403, 'error': {'message': 'Доступ с вашего IP-адреса временно ограничен', 'link': 'ru.avito://1/info/ipblock/show'}}
        except_error()
    if res['status'] != 'ok':
        # print(f'''result = {res['result']}''')
        print(f'''result = NON''')
        sys.exit(1)
    if res['status'] == 'ok':
        items_page = int(len(res['result']['items']))
        lastStamp = int(res['result']['lastStamp'])
        print(f"res['status'] == 'ok': lastStamp {lastStamp}")
        if items_page > limit_page:  # проверка на "snippet"
            items_page = items_page - 1
        for item in res['result']['items']:
            if item['type'] == 'item':
                items.append(item)
        if items_page < limit_page:
            cicle_stop = False
print(f'ITEMS Successful GET ')  # {items}')
index = 1

for i in items:  # Теперь идем по ябъявлениям:
    ad_id = str(i['value']['id'])  # ID объявления
    val = i['value']  # ID DB

    category = val['category']  # Категория

    time = val['time']  # Время публикации

    title = val['title']  # Названия

    images = ''
    price = val['price']  # Стоимость
    price = re.sub(r'[^0-9.]+', r'', price)

    address = val['address']  # Адрес

    coords = val['coords']  # Координаты

    uri = val['uri']  # URL для ПК

    uri_mweb = val['uri_mweb']  # URL для m.avito

    offer = {"url": "https://www.avito.ru" + uri_mweb, "offer_id": ad_id}
    price = ''.join(price.split())
    timestamp = datetime.fromtimestamp(time)
    timestamp = datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
    offer["date"] = timestamp
    offer["price"] = price
    offer["title"] = title
    offer["address"] = f"{coords}, {address}"
    check_database(offer)
stop_message()
