# Railway 배포 가이드

## Railway란?

**Railway**는 개발자가 애플리케이션을 쉽게 배포하고 관리할 수 있는 클라우드 플랫폼입니다.

### 주요 특징
- ✅ **무료 티어 제공**: 월 $5 크레딧 (충분한 테스트 가능)
- ✅ **간단한 배포**: Git 푸시만으로 자동 배포
- ✅ **Docker 지원**: Dockerfile 기반 배포 가능
- ✅ **환경 변수 관리**: 쉬운 설정 관리
- ✅ **자동 HTTPS**: SSL 인증서 자동 제공
- ✅ **로그 확인**: 실시간 로그 모니터링

## Railway vs 다른 플랫폼

| 특징 | Railway | Streamlit Cloud | Render | Heroku |
|------|---------|----------------|--------|--------|
| 무료 티어 | ✅ ($5/월) | ✅ | ✅ | ❌ |
| 배포 난이도 | ⭐⭐ 쉬움 | ⭐ 매우 쉬움 | ⭐⭐ 쉬움 | ⭐⭐⭐ |
| Docker 지원 | ✅ | ❌ | ✅ | ✅ |
| 자동 배포 | ✅ | ✅ | ✅ | ✅ |

## Railway 배포 단계별 가이드

### 1단계: Railway 계정 생성

1. [Railway.app](https://railway.app) 접속
2. "Start a New Project" 클릭
3. GitHub 계정으로 로그인 (권장) 또는 이메일로 가입

### 2단계: Railway CLI 설치 (선택사항)

CLI를 사용하지 않고 웹 대시보드에서도 배포 가능합니다.

```bash
# Node.js가 설치되어 있어야 합니다
npm i -g @railway/cli

# 설치 확인
railway --version
```

### 3단계: Railway 로그인

```bash
railway login
```

브라우저가 열리면 Railway 계정으로 로그인합니다.

### 4단계: 프로젝트 초기화

```bash
# 프로젝트 디렉토리로 이동
cd /Users/dhonghshimlee/Desktop/iljinGPT-agents-master

# Railway 프로젝트 초기화
railway init
```

이 명령어를 실행하면:
- Railway에서 새 프로젝트 생성
- `.railway/` 폴더 생성 (로컬 설정 저장)
- 프로젝트와 연결

### 5단계: 환경 변수 설정

```bash
# 환경 변수 추가
railway variables set OPENAI_API_KEY=your-key-here
railway variables set UPSTAGE_API_KEY=your-key-here
railway variables set TAVILY_API_KEY=your-key-here

# 또는 웹 대시보드에서 설정 가능
# Variables 탭에서 추가
```

### 6단계: 배포 설정

Railway는 자동으로 감지하지만, 명시적으로 설정할 수 있습니다.

#### 방법 1: Dockerfile 사용 (권장)

이미 `Dockerfile`이 있으므로 Railway가 자동으로 사용합니다.

#### 방법 2: Build 및 Start 명령어 설정

Railway 대시보드에서:
1. 프로젝트 클릭
2. "Settings" → "Deploy" 섹션
3. 설정:
   - **Build Command**: `pip install -r requirements.txt` (또는 `poetry install`)
   - **Start Command**: `streamlit run main.py --server.port=$PORT --server.address=0.0.0.0`

### 7단계: 배포

```bash
# 배포 실행
railway up
```

또는 GitHub에 푸시하면 자동 배포됩니다:

```bash
# Git 초기화 (아직 안 했다면)
git init
git add .
git commit -m "Initial commit"

# GitHub 리포지토리 생성 후
git remote add origin https://github.com/yourusername/iljinGPT-agents.git
git push -u origin main

# Railway에서 GitHub 리포지토리 연결하면 자동 배포됨
```

## 웹 대시보드에서 배포하기 (CLI 없이)

CLI를 사용하지 않고도 웹 대시보드에서 배포할 수 있습니다:

### 1. GitHub 리포지토리 연결

1. Railway 대시보드 접속
2. "New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. 리포지토리 선택
5. "Deploy Now" 클릭

### 2. 환경 변수 설정

1. 프로젝트 대시보드에서 "Variables" 탭 클릭
2. "New Variable" 클릭
3. 필요한 환경 변수 추가:
   - `OPENAI_API_KEY`
   - `UPSTAGE_API_KEY`
   - `TAVILY_API_KEY`
   - 기타 필요한 변수들

### 3. 배포 설정 확인

1. "Settings" 탭 클릭
2. "Deploy" 섹션 확인
3. 필요시 Build/Start 명령어 수정

## Railway 설정 파일 (선택사항)

프로젝트 루트에 `railway.json` 파일을 생성하여 설정할 수 있습니다:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "streamlit run main.py --server.port=$PORT --server.address=0.0.0.0",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 배포 후 확인

### 배포 상태 확인

```bash
# 배포 상태 확인
railway status

# 로그 확인
railway logs

# 실시간 로그
railway logs --follow
```

### 웹 대시보드에서 확인

1. Railway 대시보드에서 프로젝트 클릭
2. "Deployments" 탭에서 배포 상태 확인
3. "Logs" 탭에서 실시간 로그 확인
4. 배포 완료 후 생성된 URL 확인

## 포트 설정

Railway는 자동으로 `$PORT` 환경 변수를 제공합니다. Streamlit이 이를 사용하도록 설정되어 있습니다:

```python
# main.py 또는 Streamlit 설정
# Railway가 자동으로 PORT 환경 변수를 설정함
```

## 문제 해결

### 배포 실패 시

1. **로그 확인**:
   ```bash
   railway logs
   ```

2. **환경 변수 확인**:
   ```bash
   railway variables
   ```

3. **로컬 테스트**:
   ```bash
   # Docker로 로컬 테스트
   docker build -t iljin-gpt-agents .
   docker run -p 8501:8501 iljin-gpt-agents
   ```

### 메모리 부족 오류

- Railway 무료 티어: 512MB RAM
- 필요시 플랜 업그레이드 고려

### 타임아웃 오류

- Railway는 기본적으로 타임아웃이 없음
- 하지만 장기 실행 작업은 비동기 처리 권장

## Railway 명령어 참고

```bash
# 로그인
railway login

# 프로젝트 초기화
railway init

# 배포
railway up

# 상태 확인
railway status

# 로그 확인
railway logs
railway logs --follow  # 실시간

# 환경 변수 관리
railway variables                    # 목록 확인
railway variables set KEY=value     # 설정
railway variables delete KEY        # 삭제

# 프로젝트 정보
railway whoami                      # 현재 사용자
railway link                        # 프로젝트 연결
```

## 비용

### 무료 티어
- 월 $5 크레딧
- 충분한 테스트 및 소규모 프로덕션 사용 가능

### 유료 플랜
- 필요시 플랜 업그레이드
- 더 많은 리소스 및 기능 제공

## 다음 단계

1. ✅ Railway 계정 생성
2. ✅ 프로젝트 초기화
3. ✅ 환경 변수 설정
4. ✅ 배포 실행
5. ✅ URL 확인 및 테스트

---

**참고**: Railway는 매우 사용하기 쉬운 플랫폼입니다. CLI를 사용하지 않고도 웹 대시보드만으로 배포할 수 있습니다!


