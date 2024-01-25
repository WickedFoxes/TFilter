# tikaDir : tika-app.jar 파일이 있는 경로
tikaDir="lib/tika-app-2.9.1.jar"
# tempDir : 이미지 temp 값이 잠깐 저장되는 위치
tempDir="temp"
# uploadDir : TFilterServer에서 업로드 된 파일이 임시로 저장되는 위치
uploadTempDir = "upload_temp"
# tikaServerName : tika-server 연결 url
tikaServerName="http://localhost:9998/tika"
# tikaOCRLang : tika-server의 tesseract 언어 설정
tikaOCRLang="eng+kor"
# regularExpress : 기본으로 적용되는 정규식
regularExpress = dict()
regularExpress["social number"] = "\d\d(0[1-9]|10|11|12)(0[1-9]|[1-2][0-9]|30|31)[^\d]?[^\d]?[^\d]?[0-9]{7}"
regularExpress["phone number"] = "01[0-9][^\d]?[0-9]{4}[^\d]?[0-9]{4}"
regularExpress["e-mail"] = "[^\\s]{1,30}@[^\\s]{1,20}"