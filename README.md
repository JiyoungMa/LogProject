# LogProject

<h2>현장실습 중 진행한 로그 분석 프로젝트</h2>

- 현장실습 기간 : 2020-12-28 ~ 2021-02-26

<h3> 코드 목록 </h3>

- [Extract Data From Elastic](#extract-data-from-elastic)

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

# Extract Data From Elastic
<p style="line-height: 300%">
- Elastic Search에 저장되어있는 log data를 가져와서 하루 단위로 json 저장을 하는 코드 <br>
- 현재 설정 : client.geo.ip, django.url.full, django.request.headers.User-Agent가 있는 로그들의 timestamp, django.user.username, client.geo.ip, django.url.full, django.request.headers.User-Agent를 저장<br>
- 설정 변경 방법 : body 변수를 원하는 조건으로 변경<br>
- Log 저장 시작 날짜 변경 방법 <br>
  <: 원하는 날짜가 year-month-date,hour-minutes-seconds일 경우 <br>
    start = 'year-month-(date-1)**T**(hour-9):minutes:seconds' <br>
    end = 'year-month-date**T**(hour-9):minutes:seconds'<br>
    위와 같이 start,end의 값을 변경한다.
    시차를 고려해야 하기 때문에 hour-9를 해야한다.
 </p>
