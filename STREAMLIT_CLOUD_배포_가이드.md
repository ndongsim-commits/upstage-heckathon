# 🚀 Streamlit Cloud 배포 가이드

이 문서는 ILJIN GPT Agents를 Streamlit Cloud에 배포하는 상세한 단계별 가이드입니다.

## ✅ 사전 준비사항

- [x] GitHub 리포지토리 생성 완료: `https://github.com/ndongsim-commits/upstage-heckathon`
- [ ] GitHub에 코드 푸시 완료
- [ ] 필요한 API 키 준비:
  - `OPENAI_API_KEY`
  - `UPSTAGE_API_KEY`
  - `TAVILY_API_KEY`
  - `DEEPL_API_KEY` (선택사항)

---

## 📝 단계별 배포 가이드

### 1단계: Streamlit Cloud 접속 및 로그인

1. **[Streamlit Cloud](https://streamlit.io/cloud) 접속**
2. **"Sign in"** 버튼 클릭
3. **GitHub 계정으로 로그인** (반드시 `ndongsim-commits` 계정으로 로그인)

### 2단계: 새 앱 생성

1. Streamlit Cloud 대시보드에서 **"New app"** 버튼 클릭
2. 다음 정보 입력:
   - **Repository**: `ndongsim-commits/upstage-heckathon` 선택
   - **Branch**: `main` 선택
   - **Main file path**: `main.py` 입력
   - **App URL** (선택사항): 원하는 URL 입력 (예: `iljin-gpt-agents`)

### 3단계: 고급 설정 (중요!)

1. **"Advanced settings"** 버튼 클릭
2. **Python version**: `3.11` 선택
3. **"Secrets"** 탭 클릭
4. 다음 환경 변수들을 추가:

```toml
OPENAI_API_KEY=your-openai-api-key-here
UPSTAGE_API_KEY=your-upstage-api-key-here
TAVILY_API_KEY=your-tavily-api-key-here
DEEPL_API_KEY=your-deepl-api-key-here
```

**Secrets 입력 형식:**
- Streamlit Cloud의 Secrets는 TOML 형식입니다
- 위의 형식 그대로 복사해서 붙여넣으면 됩니다
- `your-xxx-api-key-here` 부분을 실제 API 키로 교체하세요

### 4단계: 배포 실행

1. 모든 설정이 완료되면 **"Deploy!"** 버튼 클릭
2. 배포가 시작되면 로그를 확인할 수 있습니다
3. 배포 완료까지 약 3-5분 소요됩니다

### 5단계: 배포 확인

1. 배포가 완료되면 **"View app"** 버튼이 나타납니다
2. 클릭하여 앱이 정상적으로 작동하는지 확인
3. 배포된 URL은 다음과 같은 형식입니다:
   ```
   https://iljin-gpt-agents.streamlit.app
   ```

---

## 🔧 배포 후 설정

### 환경 변수 추가/수정

1. Streamlit Cloud 대시보드에서 앱 선택
2. **"Settings"** → **"Secrets"** 클릭
3. Secrets 수정 후 **"Save"** 클릭
4. 자동으로 재배포됩니다

### 로그 확인

1. Streamlit Cloud 대시보드에서 앱 선택
2. **"Logs"** 탭 클릭
3. 실시간 로그 확인 가능

---

## ⚠️ 주의사항

### 파일 크기 제한

- **Streamlit Cloud**: 최대 1GB
- `faiss_db/` 폴더의 인덱스 파일이 크면 배포에 문제가 될 수 있습니다
- 현재 프로젝트의 인덱스 파일들이 포함되어 있으므로, 크기를 확인하세요

### 메모리 사용량

- Streamlit Cloud 무료 티어는 제한된 메모리를 제공합니다
- 대용량 모델이나 인덱스를 사용하는 경우 메모리 부족 오류가 발생할 수 있습니다

### 의존성 설치

- `requirements.txt` 파일이 올바르게 설정되어 있는지 확인하세요
- 일부 패키지가 설치되지 않으면 로그에서 확인할 수 있습니다

---

## 🆘 문제 해결

### 배포 실패 시

1. **로그 확인**: Streamlit Cloud 대시보드의 "Logs" 탭에서 오류 확인
2. **환경 변수 확인**: 모든 필수 환경 변수가 올바르게 설정되었는지 확인
3. **requirements.txt 확인**: 모든 의존성이 올바르게 나열되어 있는지 확인

### 일반적인 오류

#### 1. ModuleNotFoundError
```
ModuleNotFoundError: No module named 'xxx'
```
**해결**: `requirements.txt`에 해당 패키지가 포함되어 있는지 확인

#### 2. API Key 오류
```
API key not found
```
**해결**: Streamlit Cloud의 Secrets에 API 키가 올바르게 설정되었는지 확인

#### 3. 메모리 부족
```
MemoryError: Unable to allocate array
```
**해결**: 
- 불필요한 파일 제거
- 더 작은 모델 사용 고려
- Streamlit Cloud Pro 플랜 고려

### 로컬 테스트

배포 전에 로컬에서 테스트하는 것을 권장합니다:

```bash
# 환경 변수 설정
export OPENAI_API_KEY=your-key
export UPSTAGE_API_KEY=your-key
export TAVILY_API_KEY=your-key

# Streamlit 실행
streamlit run main.py
```

---

## 📋 체크리스트

배포 전 확인사항:

- [ ] GitHub에 코드가 푸시되었는지 확인
- [ ] `requirements.txt` 파일이 최신 상태인지 확인
- [ ] `.gitignore`에 `.env` 파일이 포함되어 있는지 확인
- [ ] 모든 필수 API 키를 준비했는지 확인
- [ ] 로컬에서 앱이 정상적으로 실행되는지 확인

---

## 🎉 배포 완료 후

배포가 완료되면:

1. ✅ 배포된 URL 확인
2. ✅ 각 페이지가 정상적으로 작동하는지 테스트:
   - Local GPT Agent
   - Document AI
   - ESRS AI
   - RBA AI
3. ✅ 환경 변수가 올바르게 설정되었는지 확인
4. ✅ 로그에서 오류가 없는지 확인

---

## 📞 추가 도움말

- [Streamlit Cloud 문서](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Cloud FAQ](https://docs.streamlit.io/streamlit-community-cloud/get-started/faqs)

---

**배포 성공을 기원합니다! 🚀**

