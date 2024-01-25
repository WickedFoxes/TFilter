# TFilter
Apache Tika를 사용하여, 파일 내 개인정보 노출을 탐색하는 프로그램

## python 라이브러리 설치
pip install -r requirements.txt

## config.py 설정
1. config.py 파일 열기
2. 본인 pc 설정에 맞게 config 경로 수정

## tika-server 실행
1. cmd 실행 후, lib 폴더로 이동
2. "java -jar tika-server-standard-2.9.1.jar --port=9998" 실행
3. "http://localhost:9998/" 접속 후, tika-server 정상 작동 확인

## TFilterServer 실행
1. cmd 실행 후, "uvicorn TFilterServer:app --reload --port=8000" 실행
2. "http://localhost:8000/docs" 접속 후 테스트 진행

## TFilterServer - /filter
- 파일을 POST 전송하여 사용함
- 파일의 본문에서 주민번호, 이메일, 휴대폰 번호를 추출함

## TFilterServer - /image
- 파일을 POST 전송하여 사용함
- 파일의 본문에 포함된 이미지를 다운로드 함