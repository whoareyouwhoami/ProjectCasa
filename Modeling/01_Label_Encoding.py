#!/usr/bin/env python
# coding: utf-8

# ---
# * 본 라벨 인코딩은 모델링에서 학습을 용이하게 하기 위한 과정으로 DB에 저장되어 있는 각 테이블의 ID와는 별개임을 밝힙니다. 사용에 유의하시기 바랍니다.

# # 라이브러리

# In[ ]:


import psycopg2
import pandas as pd
import json
import re


# # 데이터 불러오기

# In[ ]:


def call_df(table_name):
    with open('config.json', 'r') as f:
        config = json.load(f)
        
    conn = psycopg2.connect(user = config['USER'],
                              password = config['PASSWORD'],
                              host = config['HOST'],
                              port = config['PORT'],
                              database = config['DATABASE'])
    
    sql = f'SELECT * FROM {table_name}'
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df


# In[ ]:


district = call_df('crawling_db.district_table')
apartment = call_df('crawling_db.apartment_table').drop(columns='table_id')
school = call_df('crawling_db.school_table').drop(columns='table_id')
subway = call_df('crawling_db.subway_table').drop(columns='table_id')
price = call_df('crawling_db.price_table')


# # 전처리

# In[ ]:


school['school_addr_town'] = school['school_addr_town'].apply(lambda x: re.split('\d',x)[0])


# # 라벨 인코딩

# In[ ]:


import joblib
from sklearn.preprocessing import LabelEncoder
def label_encoder_save(data, var_name):
    encoder = LabelEncoder()
    encoder.fit(data[var_name])
    joblib.dump(encoder, f'./model/{var_name}_encoder.pkl')


# ## district

# In[ ]:


label_encoder_save(district, 'district_name')


# ## apartment

# In[ ]:


label_encoder_save(apartment, 'apartment_addr_town')
label_encoder_save(apartment, 'apartment_builder')
label_encoder_save(apartment, 'apartment_name')


# ## school

# In[ ]:


label_encoder_save(school, 'school_name')
label_encoder_save(school, 'school_addr_town')


# ## subway

# In[ ]:


label_encoder_save(subway, 'st_name')


# ## price
# - nothing to label
