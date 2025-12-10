# Railway 빠른 시작 가이드

Railway로 배포하는 가장 빠른 방법입니다.

## 🚀 빠른 배포 (5분 안에)

### 방법 1: 웹 대시보드 사용 (가장 쉬움)

1. **Railway 계정 생성**
   - [railway.app](https://railway.app) 접속
   - GitHub 계정으로 로그인 (권장)

2. **프로젝트 생성**
   - "New Project" 클릭
   - "Deploy from GitHub repo" 선택
   - 이 리포지토리 선택
   - "Deploy Now" 클릭

3. **환경 변수 설정**
   - 프로젝트 대시보드에서 "Variables" 탭 클릭
   - 다음 환경 변수 추가:
     ```
     OPENAI_API_KEY=your-openai-key
     UPSTAGE_API_KEY=your-upstage-key
     TAVILY_API_KEY=your-tavily-key
     ```
   - (필요한 다른 환경 변수도 추가)

4. **배포 완료 대기**
   - "Deployments" 탭에서 배포 상태 확인
   - 배포 완료 후 생성된 URL 확인

5. **접속 테스트**
   - 생성된 URL로 접속하여 앱이 정상 작동하는지 확인

### 방법 2: Railway CLI 사용

```bash
# 1. Railway CLI 설치
npm i -g @railway/cli

# 2. 로그인
railway login

# 3. 프로젝트 초기화
railway init

# 4. 환경 변수 설정
railway variables set OPENAI_API_KEY=your-key-here
railway variables set UPSTAGE_API_KEY=your-key-here
railway variables set TAVILY_API_KEY=your-key-here

# 5. 배포
railway up
```

## 📋 필요한 환경 변수

다음 환경 변수들을 Railway 대시보드의 "Variables" 탭에서 설정하세요:

- `OPENAI_API_KEY` - OpenAI API 키
- `UPSTAGE_API_KEY` - Upstage API 키 (사용하는 경우)
- `TAVILY_API_KEY` - Tavily API 키 (사용하는 경우)

(프로젝트에서 사용하는 다른 환경 변수도 추가하세요)

## 🔍 배포 확인

### 배포 상태 확인
- Railway 대시보드의 "Deployments" 탭에서 확인
- 또는 CLI: `railway status`

### 로그 확인
- Railway 대시보드의 "Logs" 탭에서 실시간 로그 확인
- 또는 CLI: `railway logs --follow`

### URL 확인
- 배포 완료 후 Railway가 자동으로 URL 생성
- "Settings" → "Domains"에서 커스텀 도메인 설정 가능

## ⚙️ 설정 파일

프로젝트에 다음 파일들이 포함되어 있습니다:

- `railway.json` - Railway 배포 설정
- `Dockerfile` - Docker 이미지 빌드 설정
- `.railwayignore` - 배포 시 제외할 파일 목록

## 🐛 문제 해결

### 배포 실패 시
1. 로그 확인: `railway logs` 또는 대시보드의 "Logs" 탭
2. 환경 변수 확인: 모든 필수 환경 변수가 설정되었는지 확인
3. Dockerfile 확인: 로컬에서 `docker build -t test .` 실행하여 테스트

### 메모리 부족
- Railway 무료 티어: 512MB RAM
- 필요시 플랜 업그레이드 고려

### 포트 오류
- Railway는 자동으로 `$PORT` 환경 변수를 설정합니다
- Dockerfile이 `$PORT`를 사용하도록 설정되어 있습니다

## 💰 비용

- **무료 티어**: 월 $5 크레딧 (충분한 테스트 가능)
- 필요시 유료 플랜으로 업그레이드 가능

## 📚 더 자세한 정보

자세한 내용은 `railway_deployment_guide.md` 파일을 참고하세요.

---

**배포 완료 후 생성된 URL을 확인하고 앱을 테스트하세요!** 🎉
