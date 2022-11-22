import time
from pymongo import MongoClient
import requests
from config import token, chat_id, admin_chat_id, mongo_string, current_db_name, collection_name

global start_time

connection = MongoClient(mongo_string)
current_db = connection[current_db_name]
collection = current_db[collection_name]


def check_database(offer):
    offer_id = offer["offer_id"]
    if (collection.find_one({'offer_id': offer_id})) is None:
        insert = {
            'url': offer["url"],
            'offer_id': offer["offer_id"],
            'date': offer["date"],
            'price': offer["price"],
            'address': offer["address"],
            'title': offer["title"]
        }
        ins_result = collection.insert_one(insert)  # добавляет одну запись в коллекцию collection
        print(ins_result.inserted_id)  # id вставленного объекта
        send_telegram(offer)
        time.sleep(2)


def start_message():
    global start_time
    start_time = time.time()
    r = requests.get(r'http://jsonip.com')
    ip = r.json()['ip']
    text = f"""{"❗New work "}{collection_name}{" started at"}
{str(time.asctime())}
{"For group: "}{chat_id}
{"Token: "}{token}
{"Server_ip: "}{ip}
{"Hestia_Web_URL: https://"}{ip}{":8083/"}"""
    print(text)
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': admin_chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url=url, data=data)
    print(response)


def stop_message():
    end_time = time.time()
    text = f"""{"✅Work "}{collection_name}{" completed at "}{str(time.asctime())}
{"lead_time="} {end_time - start_time}{"s."}"""
    print(text)
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': admin_chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url=url, data=data)
    print(response)


def format_text(offer):
    title = f"{offer['title']}"
    d = offer['date']
    date = f"{d[8:10]}.{d[5:7]} в {d[11:16]}"
    text = f"""{offer['price']} 
<a href='{offer['url']}'>{title}</a>
{offer['address']}
{date}"""
    return text


def send_telegram(offer):
    text = f"""{format_text(offer)}
{" TIME="}{str(time.asctime())}"""
    print(text)
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'HTML'
    }
    response = requests.post(url=url, data=data)
    print(response)


def main():
    pass


if __name__ == '__main__':
    main()
