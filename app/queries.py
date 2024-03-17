select_query_count_prods = "SELECT COUNT(*) FROM prods WHERE category=1;"
select_query_count_photos = "SELECT COUNT(*) FROM photos;"
select_query_count_prices = "SELECT COUNT(*) FROM prices;"
select_query_product = 'SELECT id FROM prods WHERE name = %s'
select_query_price = 'SELECT id FROM prices WHERE prod_id = %s'
select_query_price_by_name = 'SELECT id FROM prices WHERE name = %s'
select_query_photos = 'SELECT id FROM photos WHERE prod_id = %s'

insert_query_products = 'INSERT INTO prods (name, url, opis, category) VALUES (%s, %s, %s, 1)'
insert_query_photos = 'INSERT INTO photos (image, prod_id) VALUES (%s, %s)'
insert_query_prices = 'INSERT INTO prices (name, price, last_price, prod_id) VALUES (%s, %s, %s, %s)'

update_query_prices = 'UPDATE prices SET price = %s, last_price = %s WHERE prod_id = %s'
update_query_products = 'UPDATE prods SET name = %s, url = %s, opis = %s, category = 1 WHERE id = %s'
update_query_photos = 'UPDATE photos SET image = %s WHERE prod_id = %s'
