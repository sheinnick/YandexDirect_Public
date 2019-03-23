#!/usr/bin/env python
# coding: utf-8

# Скрипт Никиты Шеина https://github.com/sheinnick/  
# Качает статистику из Директа

# In[ ]:


#сделать рабочую область шире
from IPython.core.display import display, HTML
display(HTML("<style>.container { width:90% !important; }</style>"))


# In[ ]:


from datetime import datetime
import requests
from requests.exceptions import ConnectionError
from time import sleep
import json


# In[ ]:


url_yandex_direct_statistics='https://api.direct.yandex.com/json/v5/reports'


# In[ ]:


def y_direct_stat_download_report(token,DateStart,DateEnd,clientLogin='',Id='',Name='',projectname=''):
    """
    функция запрашивает и скачивает отчет из яндекс директа
    возравщает имя файла, если все прошло ок
    параметры:
    Id, Name, projectname — не обязательные. Используются только для названия файла
    clientLogin — если запрос под агентским аккаунтом, то во время вызова функции указывать обязательно. Если под клиентским, то оставлять ''
    """
    headers_y_direct_stats = {
           "Authorization": "Bearer " + token,
           "Client-Login": clientLogin,
           "Accept-Language": "ru",
           "processingMode": "auto", #auto — директ сам решает отдать в онлайн, или готовить в офлайне отчет
           "skipReportHeader": "true",
           # "skipColumnHeader": "true",  # Не выводить в отчете строку с названиями полей
           "skipReportSummary": "true"
           }

    body_y_direct_stats={
        "params": {
        "SelectionCriteria": {
            "DateFrom": DateStart,
            "DateTo": DateEnd
        },
        
        "FieldNames":  [    # вот тут можно удалять или комментить что-нибудь, если не всё нужно
#             'AdGroupId',
#             'AdGroupName',
#             'AdId',
            'AdNetworkType',
#             'Age',
#             'AvgClickPosition',
#             'AvgCpc',
#             'AvgImpressionPosition',
#             'AvgPageviews',
#             'Bounces',
            'CampaignId',
            'CampaignName',
            'CampaignType',
#             'Clicks',
#             'Conversions',
#             'Cost',
#             'Criterion',
#             'CriterionId',
#             'CriterionType',
#             'Date',
#             'Device',
#             'Gender',
            'Impressions'
#             'MobilePlatform',
#             'Slot',
#             'RlAdjustmentId'
                ],
            
        "Page": { "Limit": 1000000000},
        "ReportName": f"stats_{projectname}_{clientLogin}_{Id}_{Name}_{DateStart}_{DateEnd}",
        "ReportType": "CUSTOM_REPORT",
        "DateRangeType": "CUSTOM_DATE",
        "Format": "TSV",
        "IncludeVAT": "YES",
        "IncludeDiscount": "NO"
        }} #заканчивается  body_y_direct_stats
    
    body = json.dumps(body_y_direct_stats, indent=4) # Кодирование тела запроса в JSON
    
    #делаем запрос
    req = requests.post(url_yandex_direct_statistics, body, headers=headers_y_direct_stats)
    
    while True:
        try:
            req = requests.post(url_yandex_direct_statistics, body, headers=headers_y_direct_stats)
            req.encoding = 'utf-8'
                
            if req.status_code == 200:
                print(datetime.now())
                print('Отчет создан успешно')
                filename=f"stats_{projectname}_{clientLogin}_{Id}_{Name}_{DateStart}_{DateEnd}"+'.tsv'
                with open(filename, 'wb') as f:
                    for chunk in req.iter_content(chunk_size=1024): 
                        if chunk:
                            f.write(chunk)
                    print('file '+ filename +' downloaded')
                print(datetime.now())
                return (filename)
                
            else:
                print("Произошла ошибка")
                print('Статус код — ' + req.status_code)
                print("RequestId:  {}".format(req.headers.get("RequestId", False)))
                print("JSON-код запроса: {}".format(body))
                print("JSON-код ответа сервера: \n{}".format(u(req.json())))
                return('error')
                

        # Обработка ошибки, если не удалось соединиться с сервером API Директа
        except ConnectionError:
            # В данном случае мы рекомендуем повторить запрос позднее
            print("Произошла ошибка соединения с сервером API")
            return('error')

        # Если возникла какая-либо другая ошибка
        except:
            # В данном случае мы рекомендуем проанализировать действия приложения
            print("Произошла непредвиденная ошибка")
            return('error') 


# Вводи параметры 

# In[ ]:


token='AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA' # <<<<<<<<<<< введи токен
DateStart='2019-03-01'
DateEnd='2019-03-01'
clientLogin='' # <<<<<<<<<<< введи клиентский логин, если под агентским аккаунтом. Если под клиентским, то не трогай ;)


# Вызывай функицию

# In[ ]:


y_direct_stat_download_report(token,DateStart,DateEnd,clientLogin,'','','')


# In[ ]:




