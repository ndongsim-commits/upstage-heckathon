# n8n 설정 가이드

## 1. n8n 설치 및 실행

### 옵션 1: Docker를 사용한 설치 (권장)

```bash
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

### 옵션 2: npm을 사용한 설치

```bash
npm install n8n -g
n8n start
```

### 옵션 3: n8n Cloud 사용
[n8n Cloud](https://n8n.io/cloud)에서 계정 생성 후 사용

## 2. 워크플로우 임포트

### 2.1 기본 워크플로우 임포트
1. n8n 대시보드 접속 (기본: http://localhost:5678)
2. 왼쪽 상단 메뉴에서 "Workflows" 클릭
3. "Import from File" 클릭
4. `n8n_workflow_basic.json` 파일 선택
5. "Import" 클릭

### 2.2 고급 워크플로우 임포트 (선택사항)
1. 동일한 방법으로 `n8n_workflow_advanced.json` 파일 임포트
2. 고급 기능 (ESRS/RBA 모드 선택) 사용 시 필요

## 3. Credentials 설정

### 3.1 Upstage API Credential 설정
1. 왼쪽 메뉴에서 "Credentials" 클릭
2. "Add Credential" 클릭
3. "Upstage API" 검색 및 선택
4. 다음 정보 입력:
   - **Name**: `Upstage API` (또는 원하는 이름)
   - **API Key**: Upstage에서 발급받은 API 키
5. "Save" 클릭

### 3.2 워크플로우에 Credential 연결
1. 워크플로우 편집 화면으로 이동
2. "Upstage Solar Chat for Agent" 노드 클릭
3. "Credential to connect with" 드롭다운에서 위에서 만든 Credential 선택
4. "Upstage Document Parse" 노드도 동일하게 설정
5. "Save" 클릭

## 4. Webhook URL 확인

### 4.1 Production 모드 활성화
1. 워크플로우 편집 화면에서 오른쪽 상단 "Inactive" 토글을 "Active"로 변경
2. 또는 워크플로우 목록에서 워크플로우를 활성화

### 4.2 Webhook URL 복사
1. "Webhook" 노드 클릭
2. "Production" 탭에서 Webhook URL 확인
3. URL 복사 (예: `https://your-n8n-instance.com/webhook/iljin-gpt`)

## 5. 테스트

### 5.1 파일 없는 요청 테스트

```bash
curl -X POST https://your-n8n-instance.com/webhook/iljin-gpt \
  -H "Content-Type: application/json" \
  -d '{
    "query": "안녕하세요",
    "conversationId": "test-123"
  }'
```

예상 응답:
```json
{
  "success": true,
  "message": "ok",
  "executionId": "...",
  "data": {
    "text": "안녕하세요! 무엇을 도와드릴까요?"
  }
}
```

### 5.2 파일 포함 요청 테스트

```bash
curl -X POST https://your-n8n-instance.com/webhook/iljin-gpt \
  -F "file=@test.pdf" \
  -F "query=이 문서에 대해 설명해주세요" \
  -F "conversationId=test-123"
```

### 5.3 ESRS 모드 테스트

```bash
curl -X POST https://your-n8n-instance.com/webhook/iljin-gpt-advanced \
  -H "Content-Type: application/json" \
  -d '{
    "query": "ESRS에 대해 알려주세요",
    "conversationId": "test-123",
    "mode": "esrs"
  }'
```

### 5.4 RBA 모드 테스트

```bash
curl -X POST https://your-n8n-instance.com/webhook/iljin-gpt-advanced \
  -H "Content-Type: application/json" \
  -d '{
    "query": "RBA에 대해 알려주세요",
    "conversationId": "test-123",
    "mode": "rba"
  }'
```

## 6. EWS Chat UI 연동

### 6.1 Webhook URL 등록
1. EWS Chat UI 관리 페이지 접속
2. "n8n Webhook URL" 필드에 위에서 복사한 Webhook URL 입력
3. 저장

### 6.2 요청 형식 확인
EWS Chat UI에서 다음 형식으로 요청을 보내야 합니다:

**파일 없는 경우:**
```json
{
  "query": "사용자 질문",
  "conversationId": "대화 ID"
}
```

**파일 있는 경우:**
- Content-Type: `multipart/form-data`
- 필드:
  - `file`: 파일 데이터
  - `query`: 질문 텍스트
  - `conversationId`: 대화 ID (선택사항)

## 7. 문제 해결

### 7.1 Webhook이 응답하지 않는 경우
- 워크플로우가 활성화되어 있는지 확인
- "Production" 모드인지 확인
- n8n 로그 확인: `docker logs n8n` 또는 n8n 콘솔 확인

### 7.2 API 인증 오류
- Upstage API 키가 올바른지 확인
- Credential이 워크플로우 노드에 연결되어 있는지 확인

### 7.3 파일 파싱 오류
- 파일 형식이 지원되는지 확인 (PDF, 이미지)
- 파일 크기가 제한을 초과하지 않는지 확인
- Upstage Document Parsing API 상태 확인

### 7.4 메모리 오류
- Simple Memory 노드의 메모리 크기 제한 확인
- 대화 기록이 너무 많은 경우 정리 필요

## 8. 모니터링

### 8.1 실행 기록 확인
1. 워크플로우 목록에서 워크플로우 클릭
2. "Executions" 탭에서 실행 기록 확인
3. 실패한 실행 클릭하여 상세 로그 확인

### 8.2 성능 모니터링
- 실행 시간 확인
- API 호출 횟수 모니터링
- 에러율 확인

## 9. 프로덕션 배포

### 9.1 보안 설정
- Webhook URL에 인증 추가 고려
- HTTPS 사용 권장
- API 키 보안 관리

### 9.2 확장성 고려
- n8n 인스턴스 확장
- 로드 밸런싱 설정
- 데이터베이스 백엔드 설정 (대화 기록 영구 저장)

### 9.3 백업
- 워크플로우 정기적 백업
- Credentials 안전하게 보관
- 설정 파일 버전 관리

## 10. 추가 리소스

- [n8n 공식 문서](https://docs.n8n.io/)
- [Upstage API 문서](https://developers.upstage.ai/)
- [n8n 커뮤니티](https://community.n8n.io/)





