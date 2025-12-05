# ILJIN GPT Agents 소개

<!-- 배포 URL이 있으면 여기에 추가 -->
<!-- https://your-deployment-url.com/ -->

![ILJIN GPT Agents 메인 화면](image-placeholder-main.png)

복잡한 문서도 구조를 이해하고, 목적에 맞는 Agent를 선택하세요.

**ILJIN GPT Agents**는 PDF와 이미지의 레이아웃을 정확히 분석하여 텍스트, 표, 이미지를 모두 이해하고, 목적별로 특화된 여러 Agent를 통해 전문적인 질의응답을 제공하는 지능형 문서 분석 AI 시스템입니다.

## 구조를 이해하는 Document AI

PDF나 이미지를 업로드하면, Document AI는 문서의 레이아웃을 분석하여 텍스트, 표, 이미지를 각각 추출하고 구조화합니다.

![Document AI 문서 업로드 화면](image-placeholder-doc-upload.png)

![Document AI 레이아웃 분석 결과](image-placeholder-layout-analysis.png)

![Document AI 질의응답 화면](image-placeholder-doc-qa.png)

### 레이아웃 분석 기반 문서 처리

일반적인 RAG 시스템은 문서를 단순히 텍스트로만 처리하지만, Document AI는 Upstage Document Parsing과 고급 레이아웃 분석을 통해 문서의 구조를 정확히 파악합니다.

- **페이지별 요소 추출**: 각 페이지에서 텍스트, 표, 이미지를 개별적으로 식별
- **표 데이터 구조화**: 표의 행과 열을 분석하여 구조화된 데이터로 변환
- **이미지 컨텍스트 이해**: 이미지와 주변 텍스트의 관계를 파악
- **다국어 지원**: 번역 기능을 통해 다국어 문서도 분석 가능

## 실시간 검색이 가능한 Local GPT Agent

Local GPT Agent는 일반적인 대화와 함께 Tavily 검색 도구를 활용하여 최신 정보를 검색하고, PDF 파일을 업로드하면 자동으로 벡터 데이터베이스를 구축합니다.

![Local GPT Agent 대화 화면](image-placeholder-local-gpt.png)

![Local GPT Agent 검색 결과](image-placeholder-search.png)

### 검색 기반 지식 확장

- **Tavily 실시간 검색**: 최신 웹 정보를 검색하여 답변에 반영
- **문서 기반 RAG**: 업로드한 PDF를 벡터화하여 문서 내 정보 검색
- **관련 질문 생성**: 검색 결과를 바탕으로 추가로 탐색할 수 있는 질문 제안
- **대화 기록 관리**: 세션 기반으로 대화 맥락 유지

## 전문 분야별 특화 Agent

ESRS AI와 RBA AI는 각각 ESRS(European Sustainability Reporting Standards)와 RBA(Responsible Business Alliance) 관련 전문 지식을 사전 구축된 인덱스 기반으로 제공합니다.

![ESRS AI 질의응답 화면](image-placeholder-esrs.png)

![RBA AI 질의응답 화면](image-placeholder-rba.png)

### 사전 구축 인덱스 기반 전문 답변

- **ESRS AI**: 지속가능성 보고 표준에 대한 전문적인 답변
- **RBA AI**: 책임 있는 비즈니스 연합 기준에 대한 정확한 정보 제공
- **FAISS 벡터 검색**: 고속 유사도 검색으로 관련 정보 빠르게 찾기
- **전문가 수준 답변**: 해당 분야의 정확하고 상세한 정보 제공

## System Architecture

### Document Processing Pipeline

문서를 업로드하면, Document AI는 다음의 단계를 거쳐 지식 그래프에 저장합니다.

1. **Parsing** - Upstage `document-parse` 모델로 문서에서 텍스트, 표, 이미지 정보를 추출합니다.

2. **Layout Analysis** - PyMuPDF와 레이아웃 분석 알고리즘을 통해 페이지별 구조를 인식하고, 각 요소의 위치와 관계를 파악합니다.

3. **Element Extraction** - 텍스트, 표, 이미지를 개별적으로 추출하고 구조화합니다.
   - 텍스트: 페이지별로 추출 및 청킹
   - 표: 행과 열 구조 분석 및 데이터 추출
   - 이미지: 개별 이미지 크롭 및 저장

4. **Chunking** - 추출된 텍스트를 의미 단위로 분할합니다. RecursiveCharacterTextSplitter를 사용하여 1000자 단위로 분할하며, 50자 오버랩을 통해 문맥 손실을 최소화합니다.

5. **Embedding** - 다국어 임베딩 모델(`multilingual-e5-large-instruct`)을 사용하여 각 청크를 벡터로 변환합니다. 4096차원 벡터로 변환하여 시맨틱 검색에 활용합니다.

6. **Storage** - 문서 메타데이터, 청크, 임베딩, 페이지 정보 등을 FAISS 벡터 데이터베이스에 저장하고, BM25 키워드 인덱스와 함께 Ensemble Retriever로 관리합니다.

### Hybrid Retrieval System

정보를 검색할 때, ILJIN GPT Agents는 두 가지 검색 전략을 결합하여 최적의 결과를 찾아냅니다.

- **Vector Search (50%)**: FAISS를 활용한 벡터 유사도 검색으로 의미적으로 유사한 정보를 찾습니다. "강아지"를 검색하면 "반려견", "펫"과 같은 유사 개념도 함께 검색됩니다.

- **Keyword Search (50%)**: BM25 알고리즘을 사용한 키워드 기반 검색으로 정확한 단어가 포함된 정보를 찾습니다. 정확한 용어나 고유명사 검색에 효과적입니다.

두 검색 결과는 가중치에 따라 융합(Weighted Fusion)되어 최종 순위가 결정됩니다. Ensemble Retriever를 통해 관련성 높은 상위 k개 문서를 선택합니다.

### Multi-Agent Architecture

ILJIN GPT Agents는 목적별로 분리된 여러 Agent를 제공합니다.

| **Agent** | **목적** | **데이터 소스** | **특징** |
| --- | --- | --- | --- |
| **Document AI** | 문서 분석 및 질의응답 | 업로드된 문서 | 레이아웃 분석, 표/이미지 처리 |
| **Local GPT Agent** | 일반 대화 및 검색 | 웹 검색 + 업로드 문서 | 실시간 검색, 관련 질문 생성 |
| **ESRS AI** | ESRS 전문 답변 | 사전 구축 인덱스 | 지속가능성 보고 표준 전문 |
| **RBA AI** | RBA 전문 답변 | 사전 구축 인덱스 | 책임 있는 비즈니스 연합 전문 |

각 Agent는 독립적인 벡터 데이터베이스를 가지며, 세션 기반으로 대화 기록을 관리합니다. 사용자는 목적에 맞는 Agent를 선택하거나 동시에 여러 Agent를 활용할 수 있습니다.

### n8n Workflow Integration

EWS Chat UI와 같은 외부 시스템과의 통합을 위해 n8n 워크플로우를 제공합니다.

- **Webhook 기반 API**: RESTful API를 통해 외부 시스템에서 호출 가능
- **파일 업로드 지원**: multipart/form-data 형식으로 문서 업로드 가능
- **스트리밍 응답**: 실시간으로 응답 스트리밍 지원
- **대화 기록 관리**: conversationId 기반 세션 관리

워크플로우는 파일 포함 여부를 자동으로 감지하여 Document AI 모드 또는 일반 챗봇 모드로 자동 전환합니다.

## 유즈케이스

- **기업 문서 관리 및 분석**

계약서, 보고서, 매뉴얼 등 다양한 형식의 문서를 업로드하여 구조화된 정보로 변환하고, 자연어 질의를 통해 필요한 정보를 빠르게 찾아냅니다. 표와 이미지가 포함된 복잡한 문서도 정확히 분석합니다.

- **ESRS/RBA 준수 관리**

지속가능성 보고나 책임 있는 비즈니스 연합 기준 준수를 위해, ESRS AI와 RBA AI를 활용하여 관련 규정과 기준에 대한 전문적인 답변을 받고, 준수 사항을 확인합니다.

- **기술 문서 질의응답**

PLC 제어 시스템 매뉴얼, 기술 사양서 등 전문 문서를 업로드하여, 기술 지원 담당자가 빠르게 필요한 정보를 찾을 수 있습니다. 레이아웃 분석을 통해 표와 다이어그램도 정확히 이해합니다.

- **다국어 문서 분석**

번역 기능을 활용하여 다국어 문서를 분석하고, 원본 언어와 번역본을 모두 검색 가능한 형태로 저장하여 글로벌 팀 간 협업을 지원합니다.

- **실시간 정보 검색이 필요한 업무**

Local GPT Agent의 Tavily 검색 기능을 활용하여 최신 시장 동향, 기술 트렌드, 뉴스 등을 실시간으로 검색하고, 이를 바탕으로 의사결정을 지원합니다.

- **기업 내 지식 통합**

부서별로 흩어진 문서와 정보를 Document AI로 통합하고, 각 전문 분야별 Agent를 통해 일관된 인터페이스로 접근할 수 있습니다. n8n 연동을 통해 기존 시스템과도 쉽게 통합됩니다.
