# n8n 빠른 시작 가이드

## 5분 안에 시작하기

### 1단계: n8n 실행 (1분)
```bash
# Docker 사용
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n

# 또는 npm 사용
npm install n8n -g && n8n start
```

브라우저에서 http://localhost:5678 접속

### 2단계: 워크플로우 임포트 (1분)
1. n8n 대시보드에서 "Workflows" → "Import from File"
2. `n8n_workflow_basic.json` 파일 선택
3. "Import" 클릭

### 3단계: API 키 설정 (2분)
1. "Credentials" → "Add Credential"
2. "Upstage API" 검색 및 선택
3. Upstage API 키 입력
4. 워크플로우의 Upstage 노드들에 Credential 연결

### 4단계: 워크플로우 활성화 (30초)
1. 워크플로우 편집 화면에서 "Inactive" → "Active"로 변경
2. Webhook 노드 클릭하여 Production URL 복사

### 5단계: 테스트 (30초)
```bash
curl -X POST http://localhost:5678/webhook/iljin-gpt \
  -H "Content-Type: application/json" \
  -d '{"query": "안녕하세요", "conversationId": "test"}'
```

## 주요 파일 설명

| 파일 | 설명 |
|------|------|
| `n8n_workflow_basic.json` | 기본 워크플로우 (파일 업로드 + 일반 챗봇) |
| `n8n_workflow_advanced.json` | 고급 워크플로우 (ESRS/RBA 모드 포함) |
| `n8n_implementation_guide.md` | 상세 구현 가이드 |
| `n8n_setup_instructions.md` | 설정 및 문제 해결 가이드 |
| `n8n_env_example.env` | 환경 변수 예시 |

## 워크플로우 구조

```
Webhook (시작)
  ↓
JSCode (입력 검증)
  ↓
If (파일 체크)
  ├─ Yes → Upstage Document Parse → LLM 입력 구성
  └─ No → LLM 입력 구성
  ↓
Upstage Solar Chat Model
  ↓
Simple Memory
  ↓
AI Agent
  ↓
Respond to Webhook (끝)
```

## 요청 예시

### 일반 질문
```json
POST /webhook/iljin-gpt
Content-Type: application/json

{
  "query": "안녕하세요",
  "conversationId": "user-123"
}
```

### 파일 업로드
```bash
curl -X POST http://localhost:5678/webhook/iljin-gpt \
  -F "file=@document.pdf" \
  -F "query=이 문서를 요약해주세요" \
  -F "conversationId=user-123"
```

### ESRS 모드 (고급 워크플로우)
```json
POST /webhook/iljin-gpt-advanced
Content-Type: application/json

{
  "query": "ESRS에 대해 설명해주세요",
  "conversationId": "user-123",
  "mode": "esrs"
}
```

## 응답 형식

### 성공
```json
{
  "success": true,
  "message": "ok",
  "executionId": "...",
  "data": {
    "text": "AI 응답"
  }
}
```

### 실패
```json
{
  "success": false,
  "message": "에러 메시지",
  "executionId": "...",
  "data": {
    "errorCode": 500,
    "errorDetail": "..."
  }
}
```

## 다음 단계

1. ✅ 기본 워크플로우 테스트 완료
2. 📖 `n8n_implementation_guide.md` 읽기
3. 🔧 고급 기능 추가 (`n8n_workflow_advanced.json`)
4. 🚀 EWS Chat UI 연동
5. 📊 모니터링 및 최적화

## 문제 발생 시

1. `n8n_setup_instructions.md`의 "문제 해결" 섹션 확인
2. n8n 실행 로그 확인
3. 워크플로우 실행 기록에서 에러 상세 확인

## 추가 도움말

- 상세 가이드: `n8n_implementation_guide.md`
- 설정 가이드: `n8n_setup_instructions.md`
- n8n 공식 문서: https://docs.n8n.io/




