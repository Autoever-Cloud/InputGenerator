FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY auth_inputgenerator5.py .
EXPOSE 8080
CMD ["python", "auth_inputgenerator5.py"]
