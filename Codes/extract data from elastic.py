from elasticsearch import Elasticsearch
from matplotlib import pyplot as plt
import datetime
import json

start = '2020-12-02T15:00:00.000000' #로그를 언제부터 읽어올 것인지 : 읽어오고 싶은 날짜가 2020-12-03이면 2020-12-02T15:00:00.000000 으로 설정해야함
start = datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M:%S.%f')
end = '2020-12-03T15:00:00.000000' #start의 다음 날로 설정
end = datetime.datetime.strptime(end,'%Y-%m-%dT%H:%M:%S.%f')

es = Elasticsearch('#########')

index = '#########'

username = ""
ip = ""
cookies = ""
time = ""


while(end < datetime.datetime.now()): #오늘자 로그까지 저장함
    start = start.strftime("%Y-%m-%dT%H:%M:%S.%f")
    end = end.strftime("%Y-%m-%dT%H:%M:%S.%f")

    json_file = []

    print(start)

    #로그를 읽어올 조건
    body = {
            "size" : 1000,
            "_source": ["@timestamp","django.user.username", "client.geo.ip", "django.url.full", "django.request.headers.User-Agent"], #어떤 정보를 읽어올 것인지
            "query": {
                "bool": {
                  "must": [
                  {
                      "exists": {
                          "field": "client.geo.ip"
                      }
                  },
                  {
                      "exists": {
                          "field": "django.url.full"
                      }
                  },
                  {
                      "exists": {
                          "field": "django.request.headers.User-Agent"
                      }
                  },
                  {"range": {
                        "@timestamp": {
                        "gte": start,
                        "lt": end}
                        }}
                  ]
                }
            },
            "sort":[
              {"@timestamp" : "asc"}
              ]
            }

    #scroll을 이용해서 끝까지 로그 읽어오기
    data = []
    res = es.search(index = index, body=body, scroll='3s')
    old_scroll_id = res['_scroll_id']
    hits = res['hits']['hits']
    data.extend(hits)

    while(len(hits) == 1000):
        print(i)
        res = es.scroll(scroll_id=old_scroll_id, scroll = '3s')
        hits = res['hits']['hits']
        data.extend(hits)
        i +=1 

    #받아온 정보들을 json 형식으로 정리하기
    for users in data:
        user_data = dict()
        user_data["timestamp"] = users['_source']['@timestamp']
        user_data["ip"] = users['_source']['client']['geo']['ip']
        user_data["User-agent"] = users['_source']['django']['request']['headers']['User-Agent']
        if('user' in users['_source']['django']):
            user_data["username"] = users['_source']['django']['user']['username']
        user_data["url"] = users['_source']['django']['url']['full']

        json_file.append(user_data)
    
    file_name = end[:10]

    #json 파일로 저장
    with open('./log json/'+file_name+'.json', 'w', encoding='utf-8') as make_file:
        json.dump(json_file, make_file, indent="\t")

    start = datetime.datetime.strptime(start,'%Y-%m-%dT%H:%M:%S.%f')
    end = datetime.datetime.strptime(end,'%Y-%m-%dT%H:%M:%S.%f')

    #다음 날로 날짜 바꾸기
    start += datetime.timedelta(days=1)
    end += datetime.timedelta(days=1)