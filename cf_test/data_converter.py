import pandas as pd
import data_loader
from scipy.spatial.distance import cosine

def get_data():
	conn = data_loader.get_connection()
	data_loader.init_database(conn)
	data_loader.load_fake_data(conn)

	#data_loader.get_users(conn)
	#print(data_loader.get_all_data(conn))

	#print(pd.DataFrame(data_loader.get_all_data(conn)))
	catalogs = data_loader.get_catalogs(conn)
	print(catalogs)
	catalog_id = catalogs[0][0]
	users = data_loader.get_users(conn)
	products = data_loader.get_products(conn, catalog_id)
	user_names = [user[0] for user in users]
	product_names = [product[3] for product in products]

	users_with_products = data_loader.get_products_bought(conn, catalog_id)

	user_ids = [trans[1] for trans in users_with_products]
	product_ids = [trans[2] for trans in users_with_products]

	product_offset =max(product_ids) - min(product_ids)+1
	user_offset = max(user_ids) - min(user_ids)+1

	#print(product_offset)
	#print(user_offset)
	#print(data_loader.get_products(conn))
	#print(product_ids)

	matrix = [[0 for x in range(product_offset)] for y in range(user_offset)]
	for trans in users_with_products:
		matrix[trans[1]-min(user_ids)][trans[2]-min(product_ids)] = 1

	conn.commit()
	conn.close()

	return [user_names, product_names, matrix]
