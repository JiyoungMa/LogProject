# LogProject

<h2>현장실습 중 진행한 로그 분석 프로젝트</h2>

- 현장실습 기간 : 2020-12-28 ~ 2021-02-26

<h3> 코드 목록 </h3>

- [Extract Data From Elastic](#extract-data-from-elastic)
- [User Retention](#user-retention)
- [Users Without Login](#users-without-login)
- [Get Rid Of Duplication](#get-rid-of-duplication)
- [Users Per Id And Ids Per User](#users-per-id-and-ids-per-user)

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

- Extract Data From Elastic을 통해 생성한 json 파일과 사전에 제공받은 가입 관련 엑셀파일을 사용
- 한 주 단위로 로그인 유저들의 retention을 계산

<h3>결과</h3>
<img src="https://user-images.githubusercontent.com/50768959/141353946-98488350-7847-4977-b54d-c7c4d52f7781.png">

<br><br>

# Users Without Login

<h4> 가입 유저들 중, 로그아웃 상태로 웹사이트에 접근하는 경우가 몇 퍼센트인지 추적하는 코드</h4>

- User Retention과 동일하게 Extract Data From Elastic을 통해 생성한 json 파일과 사전에 제공받은 가입 관련 엑셀 파일을 사용
- 한 주 단위로 가입 유저들의 비로그인 사용 retention 계산

<h3>결과</h3>
<img src = "https://user-images.githubusercontent.com/50768959/141354955-cfe0a55f-d35f-43a1-9dd4-2cfed34697a6.png">

<br><br>

# Get Rid Of Duplication

<h4> 가입 유저들이 로그인 또는 비로그인 상태로 웹사이트에 접속하는 retention을 계산하는 코드</h4>

- User Retention와 Users Without Login을 통해 측정한 결과의 중복을 없애기 위한 코드

<h3>결과</h3>

<img src = "https://user-images.githubusercontent.com/50768959/141355379-4e0304a4-4b1f-403a-ac54-d403e6cc453b.png">

<br><br>

# Users Per Id And Ids Per User

<h4> 하나의 IP당 몇 명의 유저들이 있는지, 하나의 유저들이 몇 개의 IP를 사용하는지를 체크하는 코드</h4>

- 같은 ip를 몇 명의 유저들이 공유하는지, 한 유저가 몇 개의 ip를 가지고 있는지를 측정하기 위해 ip별 유저들, 유저 별 ip를 google sheet에 업로드 하는 코드

<h3>결과</h3>
<img src = "https://user-images.githubusercontent.com/50768959/141355710-0c25ac7f-7f3e-4773-ac9c-4dc09336005f.png">
<img src = "https://user-images.githubusercontent.com/50768959/141355718-099b95ff-041b-40b8-a24f-5a08f0082de4.png">
<img src = "https://user-images.githubusercontent.com/50768959/141355726-f7cba6cb-3b3c-4611-9aa7-16a817fc5214.png">
