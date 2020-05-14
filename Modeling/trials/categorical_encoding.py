# Encoding Categorical Data

import os
import pickle
import pandas as pd
from WebCrawling.database import CasaDB

pd.set_option("display.max_columns", 2000)
pd.set_option("display.width", 1000)
pd.set_option("display.max_rows", 1000)

casa = CasaDB()

def call_data(table_name):
    query = "SELECT * FROM crawling_db." + str(table_name)

    try:
        query_result = casa.db_execute(query=query, type='select')
    except:
        raise ValueError('Something wrong...')

    df = pd.DataFrame(query_result)

    return df

def save_pickle(dataframe, filename):
    pkl_dir = os.path.join(os.getcwd(), 'label_data')
    if not os.path.exists(pkl_dir):
        os.mkdir(pkl_dir)

    save_name = os.path.join(pkl_dir, filename)
    dataframe.to_pickle(save_name)

    print('Completed!')

def encode_label(dataframe, *args):
    # converting to categorical type
    try:
        for col in args:
            dataframe[col] = dataframe[col].astype('category')
    except:
        raise ValueError("Column doesn't exist....")

    # Adding labeled column
    for col in args:
        col_new = col + '_label'
        dataframe[col_new] = dataframe[col].cat.codes

    return dataframe


# crawling_db.apartment_table
#   - apartment_builder
#   - apartment_addr_town
#   - apartment_name
apartment_df = call_data(table_name='apartment_table')
apartment_result = encode_label(apartment_df, 'apartment_builder', 'apartment_addr_town', 'apartment_name')


# crawling_db.price_table
#   - area
#   - amount_original
price_df = call_data(table_name='price_table')
price_result = encode_label(price_df, 'area', 'amount_original')


# crawling_db.school_table
#   - school_addr_town
school_df = call_data(table_name='school_table')
school_result = encode_label(school_df, 'school_addr_town')


# crawling_db.subway_table
#   - st_name
subway_df = call_data(table_name='subway_table')
subway_result = encode_label(subway_df, 'st_name')


# Saving
save_pickle(apartment_result, 'apartment_table.pkl')
save_pickle(price_result, 'price_table.pkl')
save_pickle(school_result, 'school_table.pkl')
save_pickle(subway_result, 'subway_table.pkl')