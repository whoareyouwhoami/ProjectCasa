#!/usr/bin/env python
# coding: utf-8

# # 라이브러리

# In[1]:


import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


# # 역 정보 수집

# In[2]:


def SubwayInfoCrawling():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    driver = webdriver.Chrome("chromedriver.exe", options=options)
    driver.get('http://www.seoulmetro.co.kr/kr/cyberStation.do')

    source = driver.page_source
    soup = BeautifulSoup(source, 'html.parser')
    mapinfo = soup.find('div', 'mapInfo')
    lines = mapinfo.find_all('li')

    output = pd.DataFrame()
    for i in range(len(lines)):
        st_line = lines[i].span.text
        st_list = lines[i].div.text.split(',')
        for j in range(len(st_list)):
            st_name = st_list[j].strip()
            unit = pd.DataFrame({'st_name':[st_name],
                                 'st_line':[st_line]})
            output = pd.concat([output,unit], axis=0)

    output = output.reset_index(drop=True)
    driver.close()
    return output


# In[3]:


st_info = SubwayInfoCrawling()


# ## 데이터 전처리
# ### 호선명

# In[4]:


print(st_info['st_line'].unique())


# In[5]:


line_dict = {
    '분당':'분당선',
    '신분당':'신분당선',
    '경의중앙':'경의중앙선',
    '용인경전철':'에버라인',
    '우이신설경전철':'우이신설선',
    '김포':'김포골드라인'    
}


# In[6]:


st_info['st_line'] = st_info['st_line'].replace(line_dict)


# ### 역명

# In[7]:


st_info.loc[st_info['st_name']=='4·19민주묘지','st_name'] = '4.19민주묘지'
st_info.loc[st_info['st_name']=='사우(김포시청)','st_name'] = '사우'
st_info['st_name'] = st_info['st_name'].apply(lambda x: x if x[-1]=='역' else x + '역')


# # 역 주소 크롤링

# In[8]:


kakao_api_key = pd.read_csv(r'C:\Users\YHS\Google Drive\Secret\kakao.csv')
# 제 고유의 카카오 api 입니다. 헤더로 GET 해야 응답을 받을 수 있습니다.


# In[9]:


headers = {'Authorization':f"{kakao_api_key['rest_api'][0]}"}


# In[10]:


def Geocoding(st_name, st_line):
    url = f'https://dapi.kakao.com/v2/local/search/keyword.json?query={st_name} {st_line}'
    response = requests.get(url, headers=headers)
    lat = response.json()['documents'][0]['y']
    lng = response.json()['documents'][0]['x']
    return [lat,lng]


# In[11]:


st_info['coordinates'] = st_info.apply(lambda x: Geocoding(x['st_name'], x['st_line']), axis=1)


# In[12]:


st_info['st_lat'] = st_info['coordinates'].apply(lambda x: x[0])
st_info['st_lng'] = st_info['coordinates'].apply(lambda x: x[1])
st_info = st_info.drop(columns='coordinates')


# In[13]:


st_info.to_csv('./data/subway_location_info.csv', index=False)

