# 1. 베이스 이미지
FROM python:3.9-slim

# 2. 작업 디렉토리
WORKDIR /app

# 3. 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 복사
COPY service_inputgenerator1.py .

# 5. 포트 노출
EXPOSE 8080

# 6. 실행 커맨드
CMD ["python", "service_inputgenerator1.py"]
