# Vercel 배포 가이드

## ⚠️ 중요 참고사항

**Streamlit 앱을 Vercel에 배포하는 것은 권장되지 않습니다.** Vercel은 주로 서버리스 함수와 정적 사이트를 위한 플랫폼이며, Streamlit과 같은 장기 실행 애플리케이션에는 적합하지 않습니다.

### 더 나은 대안

1. **Streamlit Cloud** (가장 권장) - 무료, 간단, Streamlit 전용
2. **Railway** - 간단한 배포, Docker 지원
3. **Render** - 무료 티어 제공
4. **Fly.io** - 글로벌 배포

## Vercel 배포 방법 (제한적)

만약 Vercel에 배포해야 한다면, 다음 방법을 시도할 수 있습니다:

### 방법 1: Streamlit을 서버리스 함수로 변환 (복잡함)

Streamlit을 완전히 재작성해야 하며, 이는 큰 작업입니다.

### 방법 2: Streamlit을 별도 서버에서 실행 + Vercel 프록시

1. Streamlit 앱을 별도 서버(Railway, Render 등)에서 실행
2. Vercel에서 프록시 설정

### 방법 3: Docker + Vercel (Vercel Pro 필요)

Vercel Pro 플랜에서 Docker 컨테이너 지원을 사용할 수 있습니다.

## Streamlit Cloud 배포 (권장)

### 1단계: GitHub에 코드 푸시

```bash
# Git 초기화 (아직 안 했다면)
git init
git add .
git commit -m "Initial commit"

# GitHub에 리포지토리 생성 후
git remote add origin https://github.com/yourusername/iljinGPT-agents.git
git push -u origin main
```

### 2단계: Streamlit Cloud에 배포

1. [Streamlit Cloud](https://streamlit.io/cloud) 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 리포지토리 선택
5. 설정:
   - **Main file path**: `main.py`
   - **Python version**: `3.11`
   - **Advanced settings**:
     - Secrets: 환경 변수 추가 (API 키 등)

### 3단계: 환경 변수 설정

Streamlit Cloud의 "Secrets" 섹션에서 다음 변수들을 추가:

```
OPENAI_API_KEY=your-key
UPSTAGE_API_KEY=your-key
TAVILY_API_KEY=your-key
# 기타 필요한 API 키들
```

## Railway 배포 (대안)

### 1단계: Railway CLI 설치

```bash
npm i -g @railway/cli
railway login
```

### 2단계: 프로젝트 초기화

```bash
railway init
railway up
```

### 3단계: Railway 설정

`railway.json` 또는 Railway 대시보드에서:
- **Start Command**: `streamlit run main.py --server.port=$PORT`
- **Python Version**: `3.11`
- **Environment Variables**: API 키들 설정

## Render 배포 (대안)

### 1단계: Render 계정 생성

[Render](https://render.com) 접속 및 가입

### 2단계: 새 Web Service 생성

1. "New" → "Web Service" 클릭
2. GitHub 리포지토리 연결
3. 설정:
   - **Name**: `iljin-gpt-agents`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0`
   - **Python Version**: `3.11`

### 3단계: 환경 변수 설정

Render 대시보드의 "Environment" 섹션에서 API 키 추가

## requirements.txt 생성

Poetry를 사용 중이므로 requirements.txt를 생성해야 합니다:

```bash
# Poetry에서 requirements.txt 생성
poetry export -f requirements.txt --output requirements.txt --without-hashes

# 또는 수동으로 생성 (이미 생성됨)
```

## Docker 배포 (모든 플랫폼에서 사용 가능)

### Dockerfile 생성

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install poetry

# Poetry 설정
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# 앱 코드 복사
COPY . .

# 포트 노출
EXPOSE 8501

# Streamlit 실행
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Docker로 배포

```bash
# 이미지 빌드
docker build -t iljin-gpt-agents .

# 로컬 테스트
docker run -p 8501:8501 iljin-gpt-agents

# Docker Hub에 푸시 (선택사항)
docker tag iljin-gpt-agents yourusername/iljin-gpt-agents
docker push yourusername/iljin-gpt-agents
```

## 배포 전 체크리스트

- [ ] `.env` 파일을 `.gitignore`에 추가
- [ ] `requirements.txt` 생성 및 테스트
- [ ] 환경 변수 목록 문서화
- [ ] 파일 크기 제한 확인 (FAISS 인덱스 파일 등)
- [ ] 메모리 사용량 확인
- [ ] 타임아웃 설정 확인

## 환경 변수 예시

배포 시 필요한 환경 변수들:

```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Upstage
UPSTAGE_API_KEY=...

# Tavily
TAVILY_API_KEY=...

# LangSmith (선택사항)
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=iljin-gpt-agents

# 기타
DEEPL_API_KEY=...  # 번역 기능 사용 시
```

## 파일 크기 제한

일부 플랫폼의 파일 크기 제한:
- **Streamlit Cloud**: 1GB
- **Railway**: 500MB (무료), 더 큰 플랜 가능
- **Render**: 100MB (무료), 더 큰 플랜 가능

**주의**: `faiss_db/` 폴더의 인덱스 파일들이 크면 배포에 문제가 될 수 있습니다.

## 추천 배포 플랫폼 비교

| 플랫폼 | 무료 티어 | 배포 난이도 | Streamlit 지원 | 추천도 |
|--------|----------|------------|---------------|--------|
| Streamlit Cloud | ✅ | ⭐ 매우 쉬움 | ✅ 전용 | ⭐⭐⭐⭐⭐ |
| Railway | ✅ | ⭐⭐ 쉬움 | ✅ | ⭐⭐⭐⭐ |
| Render | ✅ | ⭐⭐ 쉬움 | ✅ | ⭐⭐⭐⭐ |
| Heroku | ❌ | ⭐⭐⭐ 보통 | ✅ | ⭐⭐⭐ |
| Fly.io | ✅ | ⭐⭐⭐ 보통 | ✅ | ⭐⭐⭐ |
| Vercel | ✅ | ⭐⭐⭐⭐ 어려움 | ❌ 제한적 | ⭐ |

## 빠른 시작: Streamlit Cloud

가장 빠르고 쉬운 방법:

```bash
# 1. GitHub에 푸시
git add .
git commit -m "Ready for deployment"
git push

# 2. Streamlit Cloud에서 배포
# https://streamlit.io/cloud 접속
# GitHub 리포지토리 연결
# main.py 선택
# 배포 완료! 🎉
```

## 문제 해결

### 메모리 부족 오류
- 큰 모델이나 인덱스 파일 제거 고려
- 더 작은 모델 사용
- 플랫폼 업그레이드

### 타임아웃 오류
- 장기 실행 작업을 비동기로 처리
- 타임아웃 설정 증가 (플랫폼 허용 시)

### 의존성 설치 실패
- `requirements.txt`에서 문제가 되는 패키지 제거
- 대체 패키지 사용
- 플랫폼별 제한 확인

---

**결론**: Streamlit 앱은 **Streamlit Cloud**나 **Railway/Render**를 사용하는 것을 강력히 권장합니다. Vercel은 Streamlit 앱에 적합하지 않습니다.
