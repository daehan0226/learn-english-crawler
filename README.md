## Learn-English-Crawler

### 소개
* 유명 사전 웹사이트에서 구동사의 뜻과 예제 데이터를 수집하여 저장

### 주요 기능
* aiohttp를 통한 비동기 크롤러 실행
* [클라이언트][클라이언트레포]에서 관리자가 [서버][서버레포]로 구동사를 생성 요청을 하면 서버에서 크롤러 스크립트 실행
* 크롤링하여 수집된 데이터는 [서버][서버레포]의 MongoDB에 저장 


[클라이언트레포]: https://github.com/daehan0226/learn-english
[서버레포]: https://github.com/daehan0226/learn-english-server
