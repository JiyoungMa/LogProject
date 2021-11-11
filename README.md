# LogProject

<h2>현장실습 중 진행한 로그 분석 프로젝트</h2>

- 현장실습 기간 : 2020-12-28 ~ 2021-02-26

<h3> 코드 목록 </h3>

- [Extract Data From Elastic](#extract-data-from-elastic)
- [User Retention](#user-retention)


<h3>프로젝트 환경 설정</h3>

|tools|version|
|-----|-------|
|Python|3.7.1|
|openpyxl|2.5.12|
|user-agents|2.2.0|
|elasticsearch|7.10.1|
|google-api-core|1.24.1|
|google-api-python-client|1.12.8|
|google-auth|1.24.0|
|google-auth-httplib2|0.0.4|
|google-auth-oauthlib|0.4.2|
|googleapis-common-protos|1.52.0|

<br><br>

# Extract Data From Elastic

<h4>Elastic Search에 저장되어있는 log data를 가져와서 하루 단위로 json 저장을 하는 코드</h4>

- 현재 설정 : client.geo.ip, django.url.full, django.request.headers.User-Agent가 있는 로그들의 timestamp, django.user.username, client.geo.ip, django.url.full, django.request.headers.User-Agent를 저장<br><br>
- 설정 변경 방법 : body 변수를 원하는 조건으로 변경<br><br>
- Log 저장 시작 날짜 변경 방법 <br><br>
  : 원하는 날짜가 year-month-date,hour-minutes-seconds일 경우 <br><br>
    start = 'year-month-(date-1)**T**(hour-9):minutes:seconds' <br><br>
    end = 'year-month-date**T**(hour-9):minutes:seconds'<br><br>
    위와 같이 start,end의 값을 변경한다.<br><br>
    시차를 고려해야 하기 때문에 hour-9를 해야한다.<br>

<br><br>

# User Retention

<h4>한 주 동안 가입한 유저들이 얼마나 로그인을 유지하고 웹사이트에 접속하는지 한 주 단위로 추적하는 코드</h4>
![image](https://user-images.githubusercontent.com/50768959/141353730-cebffe20-43c9-4662-8767-22ed50ec484e.png)
![UserRetention](https://user-images.githubusercontent.com/50768959/141353946-98488350-7847-4977-b54d-c7c4d52f7781.png)
