# 베이스 이미지 설정
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# requirements.txt 파일을 컨테이너로 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 모든 소스 파일을 컨테이너로 복사
COPY . .

# Flask 서버 실행
CMD ["python", "app.py"]


