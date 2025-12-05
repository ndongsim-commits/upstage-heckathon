# n8n 워크플로우 구현 가이드

## 개요
이 문서는 iljinGPT-agents 시스템의 기능을 n8n 워크플로우로 구현하기 위한 단계별 가이드를 제공합니다.

## 시스템 기능 분석

### 1. Local GPT Agent
- **기능**: 일반적인 챗봇 기능
- **특징**: 
  - Tavily 검색 도구 사용
  - 관련 정보 생성 기능
  - 대화 기록 관리
  - 파일 업로드 지원 (PDF RAG)

### 2. Document AI
- **기능**: 문서 분석 및 질의응답
- **특징**:
  - PDF/이미지 파일 업로드
  - 레이아웃 분석
  - 문서 파싱 및 텍스트 추출
  - 번역 기능
  - RAG 기반 질의응답

### 3. ESRS AI
- **기능**: ESRS 관련 질의응답
- **특징**:
  - 사전 구축된 FAISS 인덱스 사용
  - RAG 기반 답변 생성

### 4. RBA AI
- **기능**: RBA 관련 질의응답
- **특징**:
  - 사전 구축된 FAISS 인덱스 사용
  - RAG 기반 답변 생성

## n8n 워크플로우 구현 단계

### 단계 1: 기본 워크플로우 구조 설정

#### 1.1 Webhook 노드 설정
- **노드 타입**: `n8n-nodes-base.webhook`
- **설정**:
  - HTTP Method: POST
  - Path: `iljin-gpt` (또는 원하는 경로)
  - Response Mode: `responseNode`
  - Binary Property Name: `file`
- **역할**: 외부 요청을 받는 진입점

#### 1.2 JSCode 노드 (입력 변수 검증)
- **노드 타입**: `n8n-nodes-base.code`
- **기능**:
  - `query` 값 보정
  - `conversationId` 생성/보정
  - 파일 존재 여부 확인 (`file` 또는 `file0`)
  - 출력: `hasFile`, `query`, `conversationId`
- **코드**: 제공된 샘플 코드 사용

#### 1.3 If 노드 (파일 포함 여부)
- **노드 타입**: `n8n-nodes-base.if`
- **조건**: `hasFile === true`
- **분기**:
  - True: 파일 처리 분기
  - False: 일반 챗봇 분기

### 단계 2: 파일 처리 분기 (파일이 있는 경우)

#### 2.1 Upstage Document Parse 노드
- **노드 타입**: `n8n-nodes-upstage.documentParsingUpstage`
- **설정**:
  - Binary Property Name: `file0`
- **역할**: 업로드된 문서를 파싱하여 텍스트 추출

#### 2.2 Set 노드 (LLM 입력 구성)
- **노드 타입**: `n8n-nodes-base.set`
- **설정**:
  - `prompt`: `[문서내용]\n{{ $json.text }}\n\n[질문]\n{{ $('Webhook').item.json.body.query }}`
  - `conversationId`: `{{ $('Webhook').item.json.body.conversationId }}`

#### 2.3 Upstage Solar Chat Model 노드
- **노드 타입**: `n8n-nodes-upstage.lmChatModelUpstage`
- **설정**:
  - Model: `solar-pro2`
- **역할**: LLM 모델 설정

#### 2.4 Simple Memory 노드
- **노드 타입**: `@n8n/n8n-nodes-langchain.memoryBufferWindow`
- **설정**:
  - Session Key: `={{ $json.conversationId }}`
- **역할**: 대화 기록 관리

#### 2.5 AI Agent 노드
- **노드 타입**: `@n8n/n8n-nodes-langchain.agent`
- **설정**:
  - Prompt Type: `define`
  - Text: `={{ $json.prompt }}`
- **역할**: AI 에이전트 실행

### 단계 3: 일반 챗봇 분기 (파일이 없는 경우)

#### 3.1 Set 노드 (LLM 입력 구성)
- **노드 타입**: `n8n-nodes-base.set`
- **설정**:
  - `prompt`: `{{ $('Webhook').item.json.body.query }}`
  - `conversationId`: `{{ $('Webhook').item.json.body.conversationId }}`

#### 3.2 Upstage Solar Chat Model 노드
- **노드 타입**: `n8n-nodes-upstage.lmChatModelUpstage`
- **설정**: 동일

#### 3.3 Simple Memory 노드
- **노드 타입**: 동일

#### 3.4 AI Agent 노드
- **노드 타입**: 동일
- **추가 설정**: 
  - 필요시 도구(Tools) 추가 가능
  - Tavily 검색 도구 연동 고려

### 단계 4: 응답 처리

#### 4.1 Respond to Webhook 노드
- **노드 타입**: `n8n-nodes-base.respondToWebhook`
- **설정**:
  - Respond With: JSON
  - Response Body: 
    ```json
    {
      "success": true,
      "message": "ok",
      "executionId": "{{ $execution.id }}",
      "data": {
        "text": "{{ $json.output }}"
      }
    }
    ```
  - Response Code: 200
- **에러 처리**: 에러 발생 시 적절한 에러 메시지 반환

## 고급 기능 구현

### 기능 1: ESRS/RBA AI 통합
파일이 없고 특정 키워드가 포함된 경우 ESRS 또는 RBA 인덱스를 사용하는 분기 추가:

1. **If 노드 추가**: 쿼리에 "ESRS" 또는 "RBA" 키워드 확인
2. **FAISS Retriever 연동**: 
   - HTTP Request 노드로 외부 API 호출
   - 또는 n8n Code 노드에서 직접 FAISS 인덱스 로드
3. **RAG 체인 구성**: 검색된 컨텍스트와 질문을 결합하여 프롬프트 생성

### 기능 2: Tavily 검색 도구 통합
AI Agent에 검색 도구 추가:

1. **HTTP Request 노드**: Tavily API 호출
2. **Tool 노드**: n8n의 Tool 기능 사용
3. **AI Agent 설정**: 도구 목록에 검색 도구 추가

### 기능 3: 다중 모드 지원
사용자가 모드를 선택할 수 있도록:

1. **Webhook 요청에 mode 파라미터 추가**
2. **Switch 노드**: 모드에 따라 다른 LLM 또는 설정 사용
3. **모드 옵션**:
   - `general`: 일반 챗봇
   - `esrs`: ESRS AI
   - `rba`: RBA AI
   - `document`: Document AI

## Webhook 요청 형식

### 기본 요청 (파일 없음)
```json
{
  "query": "사용자 질문",
  "conversationId": "optional-conversation-id",
  "mode": "general" // optional: general, esrs, rba
}
```

### 파일 포함 요청
```json
{
  "query": "이 문서에 대해 질문",
  "conversationId": "optional-conversation-id"
}
```
파일은 multipart/form-data로 전송:
- `file`: 업로드할 파일
- `query`: 질문 텍스트
- `conversationId`: 대화 ID (선택사항)

## 응답 형식

### 성공 응답
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

### 에러 응답
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

## 필요한 환경 변수 및 설정

### Upstage API 설정
- `UPSTAGE_API_KEY`: Upstage API 키
- n8n Credentials에 저장 필요

### 선택적 설정
- `TAVILY_API_KEY`: Tavily 검색 사용 시
- `OPENAI_API_KEY`: OpenAI 모델 사용 시 (선택사항)

## 배포 및 테스트

### 1. n8n 워크플로우 임포트
1. n8n 대시보드 접속
2. "Import from File" 선택
3. 제공된 JSON 파일 업로드
4. Credentials 설정 확인

### 2. Webhook URL 확인
1. Webhook 노드 클릭
2. "Production" 모드에서 Webhook URL 복사
3. EWS Chat UI에 URL 등록

### 3. 테스트
```bash
# 파일 없는 요청 테스트
curl -X POST https://your-n8n-instance.com/webhook/iljin-gpt \
  -H "Content-Type: application/json" \
  -d '{
    "query": "안녕하세요",
    "conversationId": "test-123"
  }'

# 파일 포함 요청 테스트
curl -X POST https://your-n8n-instance.com/webhook/iljin-gpt \
  -F "file=@test.pdf" \
  -F "query=이 문서에 대해 설명해주세요" \
  -F "conversationId=test-123"
```

## 주의사항

1. **파일 크기 제한**: n8n의 파일 크기 제한 확인 필요
2. **타임아웃 설정**: 문서 파싱이 오래 걸릴 수 있으므로 타임아웃 설정 확인
3. **메모리 관리**: Simple Memory 노드의 메모리 크기 제한 확인
4. **에러 처리**: 모든 노드에 에러 핸들링 설정 (`onError: continueErrorOutput`)
5. **보안**: Webhook URL을 안전하게 관리하고 필요시 인증 추가

## 다음 단계

1. 기본 워크플로우 JSON 파일 확인 (`n8n_workflow_basic.json`)
2. 고급 기능 워크플로우 확인 (`n8n_workflow_advanced.json`)
3. 환경 변수 설정 확인 (`n8n_env_example.env`)
4. 테스트 및 디버깅
5. 프로덕션 배포




