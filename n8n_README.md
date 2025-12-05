# ILJIN GPT Agents - n8n 연동 가이드

이 디렉토리는 iljinGPT-agents 시스템을 n8n 워크플로우로 구현하기 위한 모든 파일을 포함합니다.

## 📋 목차

1. [빠른 시작](#빠른-시작)
2. [파일 구조](#파일-구조)
3. [시스템 기능](#시스템-기능)
4. [워크플로우 선택](#워크플로우-선택)
5. [EWS Chat UI 연동](#ews-chat-ui-연동)

## 🚀 빠른 시작

가장 빠르게 시작하려면 [`n8n_quick_start.md`](./n8n_quick_start.md)를 참고하세요.

```bash
# 1. n8n 실행
docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n

# 2. 브라우저에서 http://localhost:5678 접속
# 3. 워크플로우 임포트: n8n_workflow_basic.json
# 4. Upstage API 키 설정
# 5. 워크플로우 활성화
# 6. Webhook URL 복사하여 EWS Chat UI에 등록
```

## 📁 파일 구조

```
.
├── n8n_README.md                    # 이 파일 (전체 개요)
├── n8n_quick_start.md               # 5분 빠른 시작 가이드
├── n8n_implementation_guide.md      # 상세 구현 가이드
├── n8n_setup_instructions.md        # 설정 및 문제 해결
├── n8n_workflow_basic.json          # 기본 워크플로우
├── n8n_workflow_advanced.json        # 고급 워크플로우
└── n8n_env_example.env              # 환경 변수 예시
```

## 🎯 시스템 기능

### 1. Local GPT Agent
- 일반적인 챗봇 기능
- Tavily 검색 도구 지원
- 대화 기록 관리

### 2. Document AI
- PDF/이미지 파일 업로드
- 문서 파싱 및 분석
- RAG 기반 질의응답

### 3. ESRS AI
- ESRS 관련 질의응답
- 사전 구축된 인덱스 사용

### 4. RBA AI
- RBA 관련 질의응답
- 사전 구축된 인덱스 사용

## 🔀 워크플로우 선택

### 기본 워크플로우 (`n8n_workflow_basic.json`)
**권장**: 처음 시작하는 경우

**기능**:
- ✅ 파일 업로드 지원
- ✅ 일반 챗봇 기능
- ✅ 대화 기록 관리

**사용 시나리오**:
- 파일이 있는 경우: 문서 분석 및 질의응답
- 파일이 없는 경우: 일반 챗봇

### 고급 워크플로우 (`n8n_workflow_advanced.json`)
**권장**: ESRS/RBA 전용 모드가 필요한 경우

**추가 기능**:
- ✅ ESRS 모드
- ✅ RBA 모드
- ✅ 일반 모드
- ✅ 파일 업로드 지원

**사용 시나리오**:
- `mode: "esrs"`: ESRS 관련 질문
- `mode: "rba"`: RBA 관련 질문
- `mode: "general"`: 일반 질문
- 파일 업로드: Document AI 모드로 자동 전환

## 🔌 EWS Chat UI 연동

### Webhook URL 확인
1. n8n 워크플로우 활성화
2. Webhook 노드 클릭
3. Production URL 복사
   - 예: `https://your-n8n-instance.com/webhook/iljin-gpt`

### 요청 형식

#### 파일 없는 경우
```json
POST /webhook/iljin-gpt
Content-Type: application/json

{
  "query": "사용자 질문",
  "conversationId": "대화 ID (선택사항)"
}
```

#### 파일 있는 경우
```
POST /webhook/iljin-gpt
Content-Type: multipart/form-data

file: [파일 데이터]
query: "질문 텍스트"
conversationId: "대화 ID (선택사항)"
```

#### 고급 모드 (ESRS/RBA)
```json
POST /webhook/iljin-gpt-advanced
Content-Type: application/json

{
  "query": "ESRS에 대해 알려주세요",
  "conversationId": "대화 ID",
  "mode": "esrs"  // "esrs", "rba", "general"
}
```

### 응답 형식

#### 성공 응답
```json
{
  "success": true,
  "message": "ok",
  "executionId": "execution-id",
  "data": {
    "text": "AI 응답 텍스트"
  }
}
```

#### 에러 응답
```json
{
  "success": false,
  "message": "에러 메시지",
  "executionId": "execution-id",
  "data": {
    "errorCode": 500,
    "errorDetail": "상세 에러 정보",
    "node": "노드 이름",
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## 📚 문서 가이드

### 처음 시작하는 경우
1. [`n8n_quick_start.md`](./n8n_quick_start.md) - 5분 빠른 시작
2. [`n8n_setup_instructions.md`](./n8n_setup_instructions.md) - 상세 설정

### 구현 세부사항이 필요한 경우
- [`n8n_implementation_guide.md`](./n8n_implementation_guide.md) - 전체 구현 가이드

### 문제 해결이 필요한 경우
- [`n8n_setup_instructions.md`](./n8n_setup_instructions.md) - 문제 해결 섹션

## 🔧 필수 설정

### 1. Upstage API 키
- [Upstage 개발자 포털](https://developers.upstage.ai/)에서 API 키 발급
- n8n Credentials에 등록 필요

### 2. 선택적 설정
- **Tavily API**: 검색 기능 사용 시
- **OpenAI API**: OpenAI 모델 사용 시 (선택사항)

## 🧪 테스트

### 기본 테스트
```bash
# 일반 질문
curl -X POST http://localhost:5678/webhook/iljin-gpt \
  -H "Content-Type: application/json" \
  -d '{"query": "안녕하세요", "conversationId": "test"}'

# 파일 업로드
curl -X POST http://localhost:5678/webhook/iljin-gpt \
  -F "file=@test.pdf" \
  -F "query=이 문서를 요약해주세요" \
  -F "conversationId=test"
```

### 고급 기능 테스트
```bash
# ESRS 모드
curl -X POST http://localhost:5678/webhook/iljin-gpt-advanced \
  -H "Content-Type: application/json" \
  -d '{"query": "ESRS에 대해 알려주세요", "mode": "esrs"}'

# RBA 모드
curl -X POST http://localhost:5678/webhook/iljin-gpt-advanced \
  -H "Content-Type: application/json" \
  -d '{"query": "RBA에 대해 알려주세요", "mode": "rba"}'
```

## 📊 워크플로우 구조

### 기본 워크플로우
```
Webhook
  ↓
JSCode (입력 검증)
  ↓
If (파일 체크)
  ├─ 파일 있음 → Document Parse → LLM 입력 구성
  └─ 파일 없음 → LLM 입력 구성
  ↓
Upstage Solar Chat Model
  ↓
Simple Memory
  ↓
AI Agent
  ↓
Respond to Webhook
```

### 고급 워크플로우
```
Webhook
  ↓
JSCode (입력 검증)
  ↓
If (파일 체크)
  ├─ 파일 있음 → Document Parse → LLM 입력 구성
  └─ 파일 없음 → Switch (Mode 선택)
      ├─ ESRS → LLM 입력 구성 (ESRS)
      ├─ RBA → LLM 입력 구성 (RBA)
      └─ 일반 → LLM 입력 구성 (일반)
  ↓
Upstage Solar Chat Model
  ↓
Simple Memory
  ↓
AI Agent
  ↓
Respond to Webhook
```

## ⚠️ 주의사항

1. **파일 크기 제한**: n8n의 파일 크기 제한 확인 필요
2. **타임아웃 설정**: 문서 파싱 시간 고려
3. **메모리 관리**: 대화 기록 메모리 크기 제한 확인
4. **보안**: Webhook URL 안전하게 관리
5. **에러 처리**: 모든 노드에 에러 핸들링 설정됨

## 🆘 지원

- **문서**: 각 가이드 파일 참고
- **n8n 공식 문서**: https://docs.n8n.io/
- **Upstage 문서**: https://developers.upstage.ai/

## 📝 체크리스트

배포 전 확인사항:

- [ ] n8n 설치 및 실행 확인
- [ ] 워크플로우 임포트 완료
- [ ] Upstage API 키 설정 완료
- [ ] Credential 연결 확인
- [ ] 워크플로우 활성화 확인
- [ ] Webhook URL 확인 및 복사
- [ ] 기본 테스트 통과
- [ ] 파일 업로드 테스트 통과
- [ ] EWS Chat UI 연동 완료
- [ ] 프로덕션 환경 설정 확인

## 🎉 다음 단계

1. ✅ 기본 워크플로우 설정 완료
2. 🔧 고급 기능 추가 (선택사항)
3. 🚀 EWS Chat UI 연동
4. 📊 모니터링 설정
5. 🔒 보안 강화
6. 📈 성능 최적화

---

**마지막 업데이트**: 2024년
**버전**: 1.0.0





