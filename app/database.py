import mysql.connector
import os
from dataclasses import dataclass
import dotenv

import re

from app.models import Item
from app.misc import *
from app.queries import *

dotenv.load_dotenv()


def get_count(cursor):
    cursor.execute(select_query_count_prods)
    count1 = cursor.fetchone()
    cursor.execute(select_query_count_photos)
    count2 = cursor.fetchone()
    cursor.execute(select_query_count_prices)
    count3 = cursor.fetchone()
    print(count1[0], count2[0], count3[0])


def upload(items: list[Item]):
    # try:
    if True:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor(buffered=True)

        print('------')
        get_count(cursor)
        item = items[0]
        item.title = item.title.replace('™', '').replace('®', '')
        item.description = item.description.replace('™', '').replace('®', '')
        item.link = transliterate_cyrillic_to_latin(item.title)
        prod_id = product_not_exists(item.title, cursor)

        if prod_id is None:
            cursor.execute(insert_query_products, (item.title, item.link, item.description))
            conn.commit()
            prod_id = product_not_exists(item.title, cursor)
            cursor.execute(insert_query_photos, (item.img, prod_id))
            cursor.execute(insert_query_prices, (item.title, item.price, item.old_price, prod_id))

        else:
            cursor.execute(update_query_products,
                           (item.title, item.link, item.description, prod_id))

            price_id = price_not_exists(prod_id, cursor)
            image_id = image_not_exists(prod_id, cursor)

            if price_id is None:
                cursor.execute(insert_query_prices, (item.title, item.price, item.old_price, prod_id))
            else:
                cursor.execute(update_query_prices, (item.price, item.old_price, prod_id))

            if image_id is None:
                cursor.execute(insert_query_photos, (item.img, prod_id))
            else:
                cursor.execute(update_query_photos, (item.img, prod_id))

        prod_id = product_not_exists(item.title, cursor)
        print(item.title, prod_id)
        for item in items[1::]:
            price_id = price_not_exists_by_name(item.title, cursor)
            if price_id is None:
                cursor.execute(insert_query_prices, (item.title, item.price, item.old_price, prod_id))
            else:
                cursor.execute(update_query_prices, (item.price, item.old_price, prod_id))

        conn.commit()

    if conn.is_connected():
        cursor.close()
        conn.close()


def product_not_exists(product_name, cursor):

    cursor.execute(select_query_product, (product_name,))
    result = cursor.fetchone()
    return None if result is None else result[0]


def price_not_exists(prod_id, cursor):

    cursor.execute(select_query_price, (prod_id,))
    result = cursor.fetchone()
    return None if result is None else result[0]


def price_not_exists_by_name(title, cursor):
    cursor.execute(select_query_price_by_name, (title,))
    result = cursor.fetchone()
    return None if result is None else result[0]


def image_not_exists(prod_id, cursor):
    cursor.execute(select_query_photos, (prod_id,))
    result = cursor.fetchone()
    return None if result is None else result[0]
