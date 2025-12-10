FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 의존성 파일 복사 및 설치
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --use-deprecated=legacy-resolver -r requirements.txt

# 앱 코드 복사
COPY . .

# 포트 노출 (Railway는 동적 포트를 사용하므로 EXPOSE는 선택사항)
# Railway는 자동으로 포트를 처리하므로 EXPOSE는 필요 없지만, 명시적으로 표시
EXPOSE 8501

# Streamlit 실행 (Railway의 PORT 환경 변수 사용)
# JSON 형식으로 변경하여 Docker 경고 해결
CMD ["sh", "-c", "streamlit run main.py --server.port=${PORT:-8501} --server.address=0.0.0.0 --server.headless=true"]







