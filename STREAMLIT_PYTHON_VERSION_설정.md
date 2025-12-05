# Streamlit Cloud Python 버전 설정 가이드

## ⚠️ 중요: Python 버전 변경 필요

현재 Streamlit Cloud가 Python 3.13을 사용하고 있어 패키지 설치에 문제가 발생하고 있습니다.

## 해결 방법

### 1단계: Streamlit Cloud 대시보드 접속
1. https://share.streamlit.io 접속
2. 로그인 후 앱 선택

### 2단계: Python 버전 변경
1. 앱 대시보드에서 **"Settings"** (또는 ⚙️ 아이콘) 클릭
2. **"Advanced settings"** 섹션으로 스크롤
3. **"Python version"** 드롭다운 메뉴 찾기
4. **"3.11"** 선택
5. **"Save"** 버튼 클릭

### 3단계: 재배포
- 설정 저장 후 자동으로 재배포가 시작됩니다
- 또는 "Deploy" 버튼을 클릭하여 수동으로 재배포

## 확인 방법

재배포 후 로그에서 다음을 확인:
```
Using Python 3.11.x environment
```

Python 3.11로 변경되면 패키지 설치가 정상적으로 진행됩니다.

## 참고

- Streamlit Cloud는 `runtime.txt` 파일을 지원하지 않습니다
- Python 버전은 대시보드에서만 변경 가능합니다
- Python 3.11이 가장 안정적이고 모든 패키지와 호환됩니다

