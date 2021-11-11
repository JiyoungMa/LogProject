from elasticsearch import Elasticsearch
from matplotlib import pyplot as plt
import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import time

#google api를 사용하기 위한 설정
CREDS_FILE = '#########' #credentials.json 파일
GOOGLE_EMAIL = '#########' #google api를 사용하는 계정
SCOPES = ['#########'] #api 목록

index_range = 2
creds = None
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)


start = "2020-10-22T15:00:00.000" #계산을 시작할 주의 일요일로 설정 : 날짜가 2020-12-03이면 2020-12-02T15:00:00.000000 으로 설정해야함
start = datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M:%S.%f')
end = "2020-10-29T15:00:00.000"
end = datetime.datetime.strptime(end,'%Y-%m-%dT%H:%M:%S.%f')

user_id = dict() #각 유저가 key, ip가 value
ip_dict = dict() #각 ip가 key, 해당하는 유저가 value

#엘라스틱서치 접근 위한 설정
es = Elasticsearch('#########'')

index = '#########'

while(end < datetime.datetime.now()):
    start = start.strftime("%Y-%m-%dT%H:%M:%S.%f")
    end = end.strftime("%Y-%m-%dT%H:%M:%S.%f")

    print(start)

    #엘라스틱 서치로부터 받아올 로그의 조건
    #username과 ip가 있고 timestamp가 start와 end사이인 로그의 username과 ip를 긁어오기
    body = {
            "size" : 1000,
            "_source": ["django.user.username", "client.geo.ip"],
            "query": {
                "bool": {
                  "must": [{
                      "exists": {
                          "field": "django.user.username"
                      }
                      },
                  {
                      "exists": {
                          "field": "client.geo.ip"
                      }
                  },
                  {"range": {
                        "@timestamp": {
                        "gte": start,
                        "lt": end}
                        }}
                  ]
                }
            }
            }


    #scroll을 이용해서 끝까지 로그 읽어오기
    data = []
    res = es.search(index = index, body=body, scroll='1s')
    old_scroll_id = res['_scroll_id']
    hits = res['hits']['hits']
    data.extend(hits)
    
    index_range += len(data)
    
    while(len(hits) == 1000):
        res = es.scroll(scroll_id=old_scroll_id, scroll = '1s')
        hits = res['hits']['hits']
        data.extend(hits)


    for users in data:
        id = users['_source']['django']['user']['username']
        ip = users['_source']['client']['geo']['ip']
        if id not in user_id.keys():
            user_id[id] = [ip]
        elif ip not in user_id[id]:
            user_id[id].append(ip)

        if ip not in ip_dict.keys():
            ip_dict[ip] = [id]
        elif id not in ip_dict[ip]:
            ip_dict[ip].append(id)
    

    start = datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M:%S.%f')
    end = datetime.datetime.strptime(end,'%Y-%m-%dT%H:%M:%S.%f')

    start += datetime.timedelta(days=7)
    end += datetime.timedelta(days=7)

    del data



#Google Spread Sheet에 저장하기
SPREADSHEET_ID = '#########'

user_per_ip = 0
long_data = []
data = []
count = 0
long_count = 0
index_range = 1
long_index_range = 1
for i in ip_dict.keys():
    if count == 1000:
        request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                                range='ip!A'+str(index_range), # 2
                                                valueInputOption='RAW',
                                                body={
                                                    'values' : data
                                                })
        request.execute()
        data = []
        index_range += count
        count = 0
        time.sleep(1)

    if long_count == 1000:
        request = service.spreadsheets().values().append(spreadsheetId='#########',
                                                range='시트1!A'+str(long_index_range), # 2
                                                valueInputOption='RAW',
                                                body={
                                                    'values' : long_data
                                                })
        request.execute()
        long_data = []
        long_index_range += long_count
        long_count = 0
        time.sleep(1)
    g_data = [i]
    g_data.extend(ip_dict[i])
    user_per_ip += len(ip_dict[i])
    if len(g_data) >=6 :
        long_data.append(g_data)
        long_count +=1 
    else:
        data.append(g_data)
        count += 1

request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                                range='ip!A'+str(index_range), # 2
                                                valueInputOption='RAW',
                                                body={
                                                    'values' : data
                                                })
request.execute()

request = service.spreadsheets().values().append(spreadsheetId='#########',
                                                range='시트1!A'+str(long_index_range), # 2
                                                valueInputOption='RAW',
                                                body={
                                                    'values' : long_data
                                                })
request.execute()

print(user_per_ip/len(ip_dict.keys())) #ip당 유저 몇명인지
del data
del long_data

SPREADSHEET_ID = '#########'
data = []
long_data = []
count = 0
long_count = 0
index_range = 1
ip_per_user = 0
for i in user_id.keys():
    if count%1000 == 0:
        request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                                range='user!A'+str(index_range), # 2
                                                valueInputOption='RAW',
                                                body={
                                                    'values' : data
                                                })
        request.execute()
        data = []
        index_range += count
        count = 0
        time.sleep(1)

    if long_count == 1000:
        request = service.spreadsheets().values().append(spreadsheetId='#########',
                                                range='시트1!A'+str(long_index_range), # 2
                                                valueInputOption='RAW',
                                                body={
                                                    'values' : long_data
                                                })
        request.execute()
        long_data = []
        long_index_range += long_count
        long_count = 0
        time.sleep(1)


    g_data = [i]
    g_data.extend(user_id[i])
    ip_per_user += len(user_id[i])
    if len(g_data) >=6 :
        long_data.append(g_data)
        long_count +=1 
    else:
        data.append(g_data)
        count += 1

request = service.spreadsheets().values().append(spreadsheetId=SPREADSHEET_ID,
                                                range='user!A'+str(index_range), # 2
                                                valueInputOption='RAW',
                                                body={
                                                    'values' : data
                                                })
request.execute()

request = service.spreadsheets().values().append(spreadsheetId='#########',
                                        range='시트1!A'+str(long_index_range), # 2
                                        valueInputOption='RAW',
                                        body={
                                            'values' : long_data
                                        })
request.execute()

print(ip_per_user / len(user_id.keys())) #유저당 ip 몇개인지



long_data = []
long_index_range += long_count
long_count = 0
time.sleep(1)


del data
del user_id
del ip_dict
