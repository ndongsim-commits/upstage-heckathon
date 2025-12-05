# n8n 워크플로우 문제 해결 가이드

## 일반적인 에러 및 해결 방법

### 1. 404 에러: "The requested webhook is not registered"

**증상:**
```json
{
  "code": 404,
  "message": "The requested webhook \"POST dhongshim.lee\" is not registered."
}
```

**원인:**
- 워크플로우가 활성화되지 않음
- Webhook 경로가 잘못됨
- 워크플로우가 임포트되지 않음

**해결 방법:**

#### 1단계: 워크플로우 활성화 확인
1. n8n 대시보드 접속 (http://localhost:5678)
2. 워크플로우 목록에서 해당 워크플로우 찾기
3. 워크플로우 편집 화면으로 이동
4. 오른쪽 상단의 **"Inactive"** 토글을 **"Active"**로 변경
5. 또는 워크플로우 목록에서 직접 활성화

#### 2단계: Webhook 경로 확인
1. 워크플로우 편집 화면에서 **"Webhook"** 노드 클릭
2. **"Production"** 탭 확인
3. 표시된 URL의 경로 확인
   - 예: `http://localhost:5678/webhook/iljin-gpt`
   - 경로는 `/webhook/` 뒤의 부분입니다 (`iljin-gpt`)

#### 3단계: 올바른 경로로 요청
```bash
# 올바른 경로 사용 (워크플로우에서 설정한 경로)
curl -X POST http://localhost:5678/webhook/iljin-gpt \
  -H "Content-Type: application/json" \
  -d '{"query": "안녕", "conversationId": "test"}'
```

#### 4단계: 워크플로우 재임포트 (필요시)
1. 기존 워크플로우 삭제
2. `n8n_workflow_basic.json` 파일 다시 임포트
3. Upstage API Credential 설정 확인
4. 워크플로우 활성화

### 2. 500 에러: "요청 처리 중 오류 발생"

**증상:**
```json
{
  "success": false,
  "message": "요청 처리 중 오류 발생",
  "data": {
    "errorCode": 500
  }
}
```

**원인:**
- Upstage API 키가 설정되지 않음
- Credential이 노드에 연결되지 않음
- API 키가 잘못됨

**해결 방법:**

#### 1단계: Credential 확인
1. 왼쪽 메뉴에서 **"Credentials"** 클릭
2. **"Upstage API"** Credential이 있는지 확인
3. 없으면 생성:
   - "Add Credential" 클릭
   - "Upstage API" 검색 및 선택
   - API 키 입력
   - 저장

#### 2단계: 노드에 Credential 연결
1. 워크플로우 편집 화면으로 이동
2. **"Upstage Solar Chat for Agent"** 노드 클릭
3. **"Credential to connect with"** 드롭다운에서 Credential 선택
4. **"Upstage Document Parse"** 노드도 동일하게 설정
5. 저장

#### 3단계: API 키 확인
- Upstage 개발자 포털에서 API 키가 유효한지 확인
- API 키에 충분한 크레딧이 있는지 확인

### 3. Webhook 경로 변경 방법

워크플로우의 Webhook 경로를 변경하려면:

1. 워크플로우 편집 화면으로 이동
2. **"Webhook"** 노드 클릭
3. **"Path"** 필드 수정
   - 예: `iljin-gpt` → `dhongshim.lee`
4. 저장
5. 워크플로우 활성화 확인
6. 새로운 경로로 테스트:
   ```bash
   curl -X POST http://localhost:5678/webhook/dhongshim.lee \
     -H "Content-Type: application/json" \
     -d '{"query": "안녕", "conversationId": "test"}'
   ```

### 4. 실행 기록 확인 방법

에러의 상세 정보를 확인하려면:

1. n8n 대시보드에서 워크플로우 클릭
2. **"Executions"** 탭 클릭
3. 실패한 실행 클릭
4. 각 노드의 입력/출력 확인
5. 에러가 발생한 노드 확인

### 5. 워크플로우 상태 확인

#### 워크플로우가 활성화되어 있는지 확인:
```bash
# n8n API를 통해 확인 (선택사항)
curl http://localhost:5678/api/v1/workflows
```

또는 n8n 대시보드에서:
- 워크플로우 목록에서 활성화 상태 확인
- 초록색 점 = 활성화됨
- 회색 점 = 비활성화됨

### 6. 일반적인 체크리스트

문제 해결 전 확인사항:

- [ ] n8n이 실행 중인가? (`curl http://localhost:5678/healthz`)
- [ ] 워크플로우가 활성화되어 있는가?
- [ ] Webhook 경로가 올바른가?
- [ ] Upstage API Credential이 설정되어 있는가?
- [ ] Credential이 노드에 연결되어 있는가?
- [ ] 워크플로우가 최신 버전으로 임포트되었는가?

### 7. 디버깅 팁

#### 로그 확인
```bash
# Docker를 사용하는 경우
docker logs n8n

# npm을 사용하는 경우
# n8n 콘솔에서 로그 확인
```

#### 테스트 URL 사용
- Production URL 대신 Test URL 사용 가능
- Test URL은 워크플로우가 비활성화되어 있어도 작동
- 하지만 Production URL은 워크플로우 활성화 필수

#### 단계별 테스트
1. Webhook 노드만 테스트 (다음 노드 연결 해제)
2. JSCode 노드 출력 확인
3. 각 노드를 하나씩 활성화하며 테스트

### 8. 자주 묻는 질문 (FAQ)

**Q: Webhook 경로를 어떻게 변경하나요?**
A: Webhook 노드의 "Path" 필드를 수정하고 저장하세요.

**Q: 워크플로우를 활성화했는데도 404가 나옵니다.**
A: 
- 워크플로우를 저장했는지 확인
- 브라우저를 새로고침
- 올바른 경로를 사용하는지 확인

**Q: API 키는 어디서 얻나요?**
A: [Upstage 개발자 포털](https://developers.upstage.ai/)에서 발급받을 수 있습니다.

**Q: Production과 Test URL의 차이는?**
A:
- **Production URL**: 워크플로우가 활성화되어 있어야 작동, 실제 운영 환경에서 사용
- **Test URL**: 워크플로우가 비활성화되어 있어도 작동, 테스트용

### 9. 추가 도움말

- [n8n 공식 문서](https://docs.n8n.io/)
- [n8n 커뮤니티 포럼](https://community.n8n.io/)
- [Upstage API 문서](https://developers.upstage.ai/)

---

**마지막 업데이트**: 2024년


